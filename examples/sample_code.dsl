# Example DSL code with extended features

# Define a macro for nested loops
macro nested_for(outer_seq, inner_seq, body):
    for outer in ${outer_seq}:
        for inner in ${inner_seq}:
            ${body}

# Define a macro for pattern matching
macro match(value, *patterns):
    match ${value}:
        ${patterns}

# Define a macro for conditional statements
macro conditional(condition, true_body, false_body):
    if ${condition}:
        ${true_body}
    else:
        ${false_body}

# Define a custom DSL function for processing data
function process(data):
    result = []
    for item in ${data}:
        if item > 0:
            result.append(item * 2)
    return result

# Usage examples

# Nested loops
data = [1, 2, 3]
inner = ['a', 'b']

$nested_for(data, inner,
    print(f"{outer}-{inner}")
)

# Pattern matching
$match(point,
    case((x, y), print(f"Point: ({x}, {y})")),
    case(_, print("Not a point"))
)

# Conditional macro usage
value = 10
$conditional(value > 5,
    print("Value is greater than 5"),
    print("Value is 5 or less")
)

# Inline function calls
numbers = [-1, 0, 1, 2, 3]
processed = $process(numbers)
print(f"Processed: {processed}")

# Additional macro for range-based loops
macro range_loop(start, end, step, body):
    for i in range(${start}, ${end}, ${step}):
        ${body}

# Range loop example
$range_loop(0, 10, 2,
    print(f"Even: {i}")
)

# Macro for accumulating results
macro accumulator(data, initial, operation, result_var):
    ${result_var} = ${initial}
    for item in ${data}:
        ${result_var} = ${operation}

# Accumulator example
$accumulator([1, 2, 3, 4], 0, result + item, sum)
print(f"Sum: {sum}")

# Complex macros for defining reusable pipelines
macro pipeline(input, steps):
    current = ${input}
    ${steps}

# Pipeline usage
numbers = [1, 2, 3, 4, 5]
$pipeline(numbers,
    current = [x * 2 for x in current if x > 2],
    current = sum(current)
)
print(f"Pipeline result: {current}")
