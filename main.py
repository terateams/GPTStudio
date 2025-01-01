import epicbox

print(1111)

epicbox.configure(
    profiles=[
        epicbox.Profile('python', 'talkincode/coolstudy:latest-arm64')
    ]
)
files = [{'name': 'main.py', 'content': b'print(42)'}]
limits = {'cputime': 1, 'memory': 64}
result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
