import pyshorteners as sh
link="https://pyshorteners.readthedocs.io/en/latest/"
l=input("Enter url: ")
s=sh.Shortener()
x=(s.tinyurl.short(l))
print("Shortened url: "+x)