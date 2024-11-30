# Example DSL code

# Define a macro for nested loops
macro nested_for(outer_seq, inner_seq, body):
    for outer in ${outer_seq}:
        for inner in ${inner_seq}:
            ${body}

# Define a macro for pattern matching
macro match(value, *patterns):
    match ${value}:
        ${patterns}

# Usage example
data = [1, 2, 3]
inner = ['a', 'b']

$nested_for(data, inner,
    print(f"{outer}-{inner}")
)

$match(point,
    case((x, y), print(f"Point: ({x}, {y})")),
    case(_, print("Not a point"))
)