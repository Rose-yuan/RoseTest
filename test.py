import yaml

print(yaml.load(open("demo.yml"), Loader=yaml.FullLoader))

with open("demo3.yml","w") as f:
    print(yaml.dump(data={'a': [1, 2]}, stream=f))
