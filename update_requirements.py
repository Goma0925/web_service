import pkg_resources
import sys
#A code snippet to make a list of required libraries

#Write the modules installed in the current virtualenv into requirements.txt
print("Interpreter:")
print(sys.executable)
print("Updating the requirements.txt...")
modules = [module for module in pkg_resources.working_set]
with open("requirements1.txt", "w") as file:
    content = ""
    for i in range(len(modules)):
        content += (str(modules[i]).split(" ")[0] + "==" + str(modules[i]).split(" ")[1]) + "\n"
        print("Module:", (str(modules[i]).split(" ")[0] + "==" + str(modules[i]).split(" ")[1]))
    file.write(content)
    print("All module requirements added to requirements.txt.")
