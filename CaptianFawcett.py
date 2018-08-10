from bs4 import BeautifulSoup
import re
import csv
import pandas


#Open a local html file and load the page to bs4
url = r"C:\Users\Clarke Gallie\Desktop\Projects\Python Projects\Scrape Rockwell Stores\Stockists.html"
page = open(url)
soup = BeautifulSoup(page.read())

#Each li contains each variable we need
stores = soup.find_all('li')
stores_list =[]

# Finding Starts and Breaks
starth4 = '<h4>'
endh4 = '</h4>'
startAddress = '</svg>'
endAddress = '</p><div>'


x = 0  # counter

# Store lists of each variable
name = []
phone = []
website = []
realAddress = []
email = []

# for li in all li's
for store in stores:
    x += 1  # Counter
    store = str(store)

    print()
    print("///////////////////   Store number: ",x,"   ///////////////////")

    # Get Store Name
    storeName = store[store.find(starth4) + len(starth4):store.rfind(endh4)]  # use the breaks to find in-between texts
    newStoreName = storeName.replace('&amp;', "and")  # Replace ampersand
    name.append(newStoreName)

    # Get Address
    address = str((store[store.find(startAddress) + len(startAddress):store.rfind(endAddress)]))  # use the breaks to find in-between texts
    newaddress = address.replace('<br/>', "")  # Get rid of breaks in the HTML
    print(newaddress)
    realAddress.append(newaddress)

    # Get Phone Number
    if 'storemapper-phone' in store:
        testPhone = int(store.index('tel:'))  # Find index of the phone number
        testPhone2 = str(store[testPhone:testPhone+23])  # Add max number (23) of digits after
        if '"' in testPhone2:
            indexProblem = testPhone2.index('"')  # Find where " is after the number
            testPhone2 = testPhone2[0:indexProblem]  # Only have beg index to just before the "
            phone.append(testPhone2)
        else:
            phone.append(testPhone2)
    else:
        phone.append('N/A')  # Have to have consistent rows, not always a number there
    print(phone)

    # Get Email
    if "@" in store:  # If Email address is in this li of stores
        match = re.search(r'[\w\.-]+@[\w\.-]+', store)  # Some RegEx to get email address
        email.append(match.group(0))
    else:
        email.append('N/A')
    print(email)

    # Get URL
    if 'storemapper-url' in store:
        if 'target="_blank">h' in store:  # Look for the https websites
            urlIndex = int(store.index('target="_blank">http'))
            urlIndex2 = str(store[urlIndex:urlIndex+80])  # Start from where the website is and add 80 char
        elif 'target="_blank">w' in store:  # Same process for www websites
            urlIndex = int(store.index('target="_blank">www'))
            urlIndex2 = str(store[urlIndex:urlIndex + 80])
        if '<' in urlIndex2:  # Near the end there is a < marker, we use this to benchmark the string manipulations
            indexProblem2 = urlIndex2.index('<')  # Find the end < and keep all the text before it
            urlIndex2 = urlIndex2[0:indexProblem2]
            indexProblem3 = urlIndex2.index('>')  # Find the end > and keep all the text after it
            urlIndex2 = urlIndex2[indexProblem3+1:]
            website.append(urlIndex2)
        else:
            website.append(urlIndex2)
    else:
        website.append('N/A')
    print(website)


# Double check to make sure all the lengths are the same
print('Complete List')
print(len(realAddress))
print(len(email))
print(len(name))
print(len(website))
print(len(phone))

# Create a CSV file
# df = pandas.DataFrame(data={"col1": name, "col2": email, "col3": phone, "col4": realAddress, "col5": website})
# df.to_csv("./captainfawcett.csv", sep=',', index=False)
