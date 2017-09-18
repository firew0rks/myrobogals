# myRobogals rgwiki Requirements Document
## Aim
To provide a unified location for the organisation to share knowledge and resources between volunteers, chapters in different regions

## Description
There has been a lack of sharing resources and transfer of knowledge within the organisation. When an executive member transitions out, a lot of content and knowledge gained over the years will be lost. The idea is to create a wiki that executive members are able to add and modify content so that there is a unified place to store and view the material. The content will include but not limited to creative workshops, handover documents, how-to coding guides and documentation. They will be able to download PDF versions of the documents for their own personal references to take to workshops for example.

The architecture of the system will be that every entry will be stored as a Markdown (.md) file, thus creating a flat storage system. The user will be able to edit the documents by either using the online editor or by uploading a file and view the documents by logging into myRobogals.

## Functionality
### Users
- The ability to search for content via tags and datetime
- The ability to search sort based on uploaded date/time and rating
- The ability to download a specific document as a PDF

### Executives
- The ability to upload different versions of the same document
    - One way of doing this is to provide a template document, with Robogals-specific header items which will be removed by the system but used as version control when the document is updated
- The ability to upload a new document
- The ability to live edit a document (the preview does not have to be presented on the same page. A button can be used to Preview and Return to Edit)
- The ability to live create a document

## Design Details
### Layout
Since we are using a third party code (mdwiki), the html page (mdwiki.html) will be embedded into an iframe under the myRobogals header and search bar.

![rgwiki](img/rgwiki-layout.png)

### Index page
The index page will contain the following items:
- Newly uploaded content titles
- A weekly highlight of workshops (selected and cycled at random)
- Wiki help
- FAQ
- Search bar

![rgwiki-landing](img/rgwiki-landing-page.png)

## Coding Details
The wiki will be implemented into a new app called rgwiki. The individual markdown files will be located in a folder in rgwiki called files/md and images will be located under files/img.

### Model Components
Each markdown file that is uploaded will contain the following elements
- Tags
- Timestamp
- Version
- Uploader's name

### URL references
Since the third party app is using a unique style of referencing, the rendering of the URLs will follow that format. For example, if we're opening a document called workshop.md and depending on the pk this is stored at in the database:
- The pk of workshop.md is 1, therefore the url will be https://my.robogals.org/mdwiki.html#!files/md/1.md 
    + Note the (hashbang) #! format that follows to render that document
- Renders the document in an iframe under the header and search bar.

### Custom parser
I've found instances that the third party app will break. To ensure that this doesn't happen, a custom parser will need to be build to ensure that the document is formatted correctly and will work on the page.

# References
http://dynalon.github.io/mdwiki/#!index.md
https://github.com/Dynalon/mdwiki
