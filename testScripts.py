# Use this file to test out utility function scripts before implementing in routes functions.



mail = input("Enter email: ")
id = mail[0 : mail.index("@")]
domain = mail[mail.index("@") :]
redact = id[0:3] + ("*" * len(id[3:])) + domain
print(redact)