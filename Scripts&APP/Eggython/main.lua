print("Hello, Eggy Lua!")

-- Python interpreter in pure Lua
local PythonInterpreter = {}

-- Token constants
PythonInterpreter.Token = {
    KEYWORD   = 1,
    IDENTIFIER= 2,
    NUMBER    = 3,
    STRING    = 4,
    OPERATOR  = 5,
    NEWLINE   = 6,
    INDENT    = 7,
    DEDENT    = 8,
    EOF       = 9,
}

-- Utility: check if value exists in a table
local function table_contains(tbl, val)
    for _, v in ipairs(tbl) do
        if v == val then return true end
    end
    return false
end

-- ------------------------------------------------------------
-- Lexer: Python source -> token stream
-- ------------------------------------------------------------
function PythonInterpreter.lex(code)
    local Token = PythonInterpreter.Token
    -- split lines (preserve empty lines)
    local lines = {}
    for line in code:gmatch("([^\n]*)\n?") do
        table.insert(lines, line)
    end

    local tokens = {}
    local indent_stack = {0}   -- stack of indentation levels

    -- Tokenize a line without leading whitespace
    local function tokenize_line(line)
        local toks = {}
        local i = 1
        local n = #line
        while i <= n do
            local ch = line:sub(i, i)

            if ch == ' ' or ch == '\t' then
                i = i + 1
            elseif ch == '#' then          -- comment: ignore rest of line
                break
            elseif ch == '"' or ch == "'" then
                local quote = ch
                local j = i + 1
                while j <= n do
                    local c = line:sub(j, j)
                    if c == quote and line:sub(j-1, j-1) ~= '\\' then
                        break
                    end
                    j = j + 1
                end
                if j > n then error("Unterminated string") end
                local str = line:sub(i+1, j-1)
                table.insert(toks, {type=Token.STRING, value=str})
                i = j + 1
            elseif ch:match("%d") then
                local j = i
                while j <= n and line:sub(j, j):match("[%d%.]") do
                    j = j + 1
                end
                local num_str = line:sub(i, j-1)
                local num = tonumber(num_str)
                if not num then error("Invalid number: "..num_str) end
                table.insert(toks, {type=Token.NUMBER, value=num})
                i = j
            elseif ch:match("[a-zA-Z_]") then
                local j = i
                while j <= n and line:sub(j, j):match("[a-zA-Z0-9_]") do
                    j = j + 1
                end
                local ident = line:sub(i, j-1)
                -- 修复：Lua 表构造中不能直接使用 "if"=true 这种语法，改用方括号形式
                local keywords = {
                    ["if"] = true, ["else"] = true, ["while"] = true, ["print"] = true,
                    ["and"] = true, ["or"] = true, ["not"] = true,
                    ["True"] = true, ["False"] = true, ["None"] = true
                }
                if keywords[ident] then
                    table.insert(toks, {type=Token.KEYWORD, value=ident})
                else
                    table.insert(toks, {type=Token.IDENTIFIER, value=ident})
                end
                i = j
            else   -- operators and delimiters
                local op = ch
                if i < n then
                    local next_ch = line:sub(i+1, i+1)
                    local two_char = ch .. next_ch
                    if two_char == "<=" or two_char == ">=" or
                       two_char == "==" or two_char == "!=" then
                        op = two_char
                        i = i + 1
                    end
                end
                table.insert(toks, {type=Token.OPERATOR, value=op})
                i = i + 1
            end
        end
        return toks
    end

    -- Process each non‑empty line
    for _, line in ipairs(lines) do
        if not line:match("^%s*$") then
            -- compute indentation level (number of leading spaces)
            local indent = line:match("^%s*"):len()

            -- INDENT / DEDENT handling
            if indent > indent_stack[#indent_stack] then
                table.insert(tokens, {type=Token.INDENT, value=indent})
                table.insert(indent_stack, indent)
            elseif indent < indent_stack[#indent_stack] then
                while indent < indent_stack[#indent_stack] do
                    table.remove(indent_stack)
                    table.insert(tokens, {type=Token.DEDENT, value=indent})
                end
            end

            -- remove leading whitespace
            line = line:match("^%s*(.*)$")

            -- tokenize the line content
            local line_tokens = tokenize_line(line)
            for _, t in ipairs(line_tokens) do
                table.insert(tokens, t)
            end
            table.insert(tokens, {type=Token.NEWLINE})
        end
    end

    -- close all remaining indents
    while #indent_stack > 1 do
        table.remove(indent_stack)
        table.insert(tokens, {type=Token.DEDENT, value=0})
    end
    table.insert(tokens, {type=Token.EOF})

    return tokens
end

-- ------------------------------------------------------------
-- Parser: token stream -> AST (recursive descent)
-- ------------------------------------------------------------
function PythonInterpreter.parse(tokens)
    local Token = PythonInterpreter.Token
    local pos = 1

    local function peek()
        return tokens[pos] or {type=Token.EOF}
    end

    local function next_token()
        local t = tokens[pos]
        pos = pos + 1
        return t
    end

    local function expect(typ, val)
        local t = next_token()
        if t.type ~= typ then
            error(string.format("Expected token type %d, got %d", typ, t.type))
        end
        if val and t.value ~= val then
            error(string.format("Expected value '%s', got '%s'", val, t.value))
        end
        return t
    end

    -- forward declarations
    local parse_statement, parse_expression, parse_block
    local parse_if, parse_while, parse_print, parse_assign
    local parse_or, parse_and, parse_comparison, parse_not
    local parse_arith, parse_term, parse_factor, parse_atom

    -- ---------- expression parsing with precedence ----------
    -- lowest:  or
    --          and
    --          not
    --          comparisons (< > <= >= == !=)
    --          + -
    --          * / %
    -- highest: unary + - (and parentheses)

    function parse_or()
        local left = parse_and()
        while peek().type == Token.KEYWORD and peek().value == "or" do
            local op = next_token().value
            local right = parse_and()
            left = {type="BinOp", left=left, op=op, right=right}
        end
        return left
    end

    function parse_and()
        local left = parse_comparison()
        while peek().type == Token.KEYWORD and peek().value == "and" do
            local op = next_token().value
            local right = parse_comparison()
            left = {type="BinOp", left=left, op=op, right=right}
        end
        return left
    end

    function parse_comparison()
        local left = parse_not()
        local comp_ops = {"<", ">", "<=", ">=", "==", "!="}
        while peek().type == Token.OPERATOR and
              table_contains(comp_ops, peek().value) do
            local op = next_token().value
            local right = parse_not()
            left = {type="BinOp", left=left, op=op, right=right}
        end
        return left
    end

    function parse_not()
        if peek().type == Token.KEYWORD and peek().value == "not" then
            next_token()
            local expr = parse_not()   -- allow multiple not
            return {type="UnaryOp", op="not", operand=expr}
        else
            return parse_arith()
        end
    end

    function parse_arith()
        local left = parse_term()
        while peek().type == Token.OPERATOR and
              (peek().value == "+" or peek().value == "-") do
            local op = next_token().value
            local right = parse_term()
            left = {type="BinOp", left=left, op=op, right=right}
        end
        return left
    end

    function parse_term()
        local left = parse_factor()
        while peek().type == Token.OPERATOR and
              (peek().value == "*" or peek().value == "/" or peek().value == "%") do
            local op = next_token().value
            local right = parse_factor()
            left = {type="BinOp", left=left, op=op, right=right}
        end
        return left
    end

    function parse_factor()
        local t = peek()
        if t.type == Token.OPERATOR and (t.value == "+" or t.value == "-") then
            local op = next_token().value
            local expr = parse_factor()
            return {type="UnaryOp", op=op, operand=expr}
        else
            return parse_atom()
        end
    end

    function parse_atom()
        local t = next_token()
        if t.type == Token.NUMBER then
            return {type="Num", value=t.value}
        elseif t.type == Token.STRING then
            return {type="Str", value=t.value}
        elseif t.type == Token.IDENTIFIER then
            return {type="Name", id=t.value}
        elseif t.type == Token.KEYWORD and
               (t.value == "True" or t.value == "False" or t.value == "None") then
            return {type="Name", id=t.value}
        elseif t.type == Token.OPERATOR and t.value == "(" then
            local expr = parse_expression()
            expect(Token.OPERATOR, ")")
            return expr
        else
            error("Unexpected atom: " .. tostring(t.value))
        end
    end

    parse_expression = function() return parse_or() end

    -- ---------- statement parsing ----------
    function parse_block()
        local stmts = {}
        while peek().type ~= Token.DEDENT and peek().type ~= Token.EOF do
            local stmt = parse_statement()
            table.insert(stmts, stmt)
        end
        return stmts
    end

    function parse_if()
        next_token()   -- 'if'
        local test = parse_expression()
        expect(Token.OPERATOR, ':')
        expect(Token.NEWLINE)
        expect(Token.INDENT)
        local body = parse_block()
        expect(Token.DEDENT)

        local orelse = nil
        if peek().type == Token.KEYWORD and peek().value == "else" then
            next_token()
            expect(Token.OPERATOR, ':')
            expect(Token.NEWLINE)
            expect(Token.INDENT)
            orelse = parse_block()
            expect(Token.DEDENT)
        end
        return {type="If", test=test, body=body, orelse=orelse}
    end

    function parse_while()
        next_token()   -- 'while'
        local test = parse_expression()
        expect(Token.OPERATOR, ':')
        expect(Token.NEWLINE)
        expect(Token.INDENT)
        local body = parse_block()
        expect(Token.DEDENT)
        return {type="While", test=test, body=body}
    end

    function parse_print()
        next_token()   -- 'print'
        expect(Token.OPERATOR, '(')
        local expr = parse_expression()
        expect(Token.OPERATOR, ')')
        expect(Token.NEWLINE)
        return {type="Print", value=expr}
    end

    function parse_assign()
        local ident = next_token()   -- IDENTIFIER
        expect(Token.OPERATOR, '=')
        local expr = parse_expression()
        expect(Token.NEWLINE)
        return {type="Assign", target=ident.value, value=expr}
    end

    parse_statement = function()
        local t = peek()
        if t.type == Token.KEYWORD then
            if t.value == "if" then
                return parse_if()
            elseif t.value == "while" then
                return parse_while()
            elseif t.value == "print" then
                return parse_print()
            else
                error("Unsupported keyword: " .. t.value)
            end
        elseif t.type == Token.IDENTIFIER then
            return parse_assign()
        else
            error("Unexpected token at statement start: " .. tostring(t.value))
        end
    end

    -- program entry
    local function parse_program()
        local statements = {}
        while peek().type ~= Token.EOF do
            local stmt = parse_statement()
            table.insert(statements, stmt)
        end
        return {type="Program", body=statements}
    end

    return parse_program()
end

-- ------------------------------------------------------------
-- Evaluator: AST -> execution
-- ------------------------------------------------------------
function PythonInterpreter.is_truthy(val)
    if val == nil then return false end
    if type(val) == "boolean" then return val end
    if type(val) == "number" then return val ~= 0 end
    if type(val) == "string" then return #val > 0 end
    return true   -- tables and other objects are truthy
end

function PythonInterpreter.eval(ast, env)
    if ast.type == "Program" then
        for _, stmt in ipairs(ast.body) do
            PythonInterpreter.eval(stmt, env)
        end
        return nil
    elseif ast.type == "Assign" then
        local val = PythonInterpreter.eval(ast.value, env)
        env[ast.target] = val
        return val
    elseif ast.type == "Print" then
        local val = PythonInterpreter.eval(ast.value, env)
        env.print(val)
        return val
    elseif ast.type == "If" then
        local test_val = PythonInterpreter.eval(ast.test, env)
        if PythonInterpreter.is_truthy(test_val) then
            PythonInterpreter.eval({type="Program", body=ast.body}, env)
        elseif ast.orelse then
            PythonInterpreter.eval({type="Program", body=ast.orelse}, env)
        end
        return nil
    elseif ast.type == "While" then
        while PythonInterpreter.is_truthy(PythonInterpreter.eval(ast.test, env)) do
            PythonInterpreter.eval({type="Program", body=ast.body}, env)
        end
        return nil
    elseif ast.type == "BinOp" then
        local left = PythonInterpreter.eval(ast.left, env)
        local right = PythonInterpreter.eval(ast.right, env)
        if ast.op == "+" then return left + right
        elseif ast.op == "-" then return left - right
        elseif ast.op == "*" then return left * right
        elseif ast.op == "/" then return left / right
        elseif ast.op == "%" then return left % right
        elseif ast.op == "<" then return left < right
        elseif ast.op == ">" then return left > right
        elseif ast.op == "<=" then return left <= right
        elseif ast.op == ">=" then return left >= right
        elseif ast.op == "==" then return left == right
        elseif ast.op == "!=" then return left ~= right
        elseif ast.op == "and" then
            if not PythonInterpreter.is_truthy(left) then
                return left
            else
                return PythonInterpreter.eval(ast.right, env)
            end
        elseif ast.op == "or" then
            if PythonInterpreter.is_truthy(left) then
                return left
            else
                return PythonInterpreter.eval(ast.right, env)
            end
        else
            error("Unknown binary operator: " .. ast.op)
        end
    elseif ast.type == "UnaryOp" then
        local operand = PythonInterpreter.eval(ast.operand, env)
        if ast.op == "+" then return operand
        elseif ast.op == "-" then return -operand
        elseif ast.op == "not" then
            return not PythonInterpreter.is_truthy(operand)
        else error("Unknown unary operator: " .. ast.op) end
    elseif ast.type == "Num" then
        return ast.value
    elseif ast.type == "Str" then
        return ast.value
    elseif ast.type == "Name" then
        if ast.id == "True" then return true
        elseif ast.id == "False" then return false
        elseif ast.id == "None" then return nil
        else
            local val = env[ast.id]
            if val == nil then
                error("Undefined variable: " .. ast.id)
            end
            return val
        end
    else
        error("Unknown AST node type: " .. ast.type)
    end
end

-- ------------------------------------------------------------
-- Public API: run Python code
-- ------------------------------------------------------------
function PythonInterpreter.run(code)
    local tokens = PythonInterpreter.lex(code)
    local ast = PythonInterpreter.parse(tokens)
    local env = {
        print = function(...) print(...) end,
        True = true,
        False = false,
    }
    PythonInterpreter.eval(ast, env)
end

-- ------------------------------------------------------------
-- Example usage
-- ------------------------------------------------------------
local example_code = [[
a = 10
b = 20
if a < b:
    print(a)
    print(b)
else:
    print("no")

x = 5
y = 2
print(x * y + 1)

i = 0
while i < 3:
    print(i)
    i = i + 1
]]

print("=== Running Python code ===")
PythonInterpreter.run(example_code)
