def func_to_test(env, instances):
	if env == "prod":
		print("This is the env: " + env)
		print("This is the instances: " + instances)
	#else:
	#	print("this is the else")

env = input("What is your env: ")
instance = "test1"

func_to_test(env, instance)
print("end")
