# Rihal CodeStacker Challenge Backend

This repository contains my code submitted for the Backend CodeStacker Challenge by [Rihal](https://rihal.om/).

**Note -** This repository only contains the back end code - the React front end can be found [here](https://github.com/HishamAl-Harrasi/RihalCodeStacker-Frontend).

### Backend Challenge:
The back end challenge was to create a tool which takes in a number of resumes and finds the resumes which contain the keywords inputted by the user.

For example, if the user was looking for React developers, they would insert the resumes they want to check, and enter in the keyword "*React*". The application would then show the user which resumes contain the keyword on the front end.

The back end first parses the inputted resume (which is required to be a PDF), and then utilises a regex based approach to find if any of the text in the resume contains any of the inputted keywords.

The back end also checks that the inputted resume files are in a PDF format, by checking that the HTTP `Content-Type` header is set to `application/pdf`, as well as checking the inputted files MIME type, further ensuring that the file is a PDF.
