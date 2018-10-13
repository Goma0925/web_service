import pkg_resources

#Write the modules installed in the current virtual env into requirements.txt
modules = [module for module in pkg_resources.working_set]
with open("requirements.txt", "w") as file:
    content = ""
    for i in range(len(modules)):
        content += (str(modules[i]).split(" ")[0] + "==" + str(modules[i]).split(" ")[1]) + "\n"
    file.write(content)
    print("All modules added to requirements.txt.")

