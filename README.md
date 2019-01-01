# i-reporter
[![Build Status](https://travis-ci.com/Anguandia/iReporter_app.svg?branch=develop)](https://travis-ci.com/Anguandia/iReporter_app)
[![Coverage Status](https://coveralls.io/repos/github/Anguandia/i-reporter/badge.svg?branch=develop)](https://coveralls.io/github/Anguandia/i-reporter?branch=develop)
Back end for an on-line events flagging API

INTRODUCTION 
This is the server side implementation of an online events logging system meant to work with any user interface that will communicate through JSON.

Main functionality
The application takes in client data to produce and store public concern alerts sent in that can the be retrieved, some fields updated and records deleted.

URLs
The application can create, retrieve, update and delete individual records and additionally retrieve all records
These functions are exposed through defined URL routes as explained in the details section here under

Scope
The application has no user component, authentication or authorization in this version but provides for full manipulation of records

User experience:
User experience is at the core of the design.The application furnishes informative responses to every request, pointing out possible errors in requests if not executed.
responses are of two general categories; request success feedback and error responses, each producing the response code, requested resource (if required and successful) and the appropriate response message

ROUTES OPERATIONS AND BEHAVIORS
1. Create red-flag:
URL: POST/api/v1/red_flags
The request body MUST at the very minimum contain values for red-flag properties of location, comment, and createdBy.
Location: name of the place of occurrence of the alert event
Comment: description of the event being reported
CreatedBy: Identity of the user raising the alert. This will become fully automated when the user module is incorporated,as of this version, only any integer input will work
If any of the three properties is missed, miss spelled, value not provided or value of wrong type provided, a corresponding response will be returned. Else, the record is created, with additional attributes filled with defaults and success response message returned.
Of the remaining attributes, type(for record type), image and video can be explicitly supplied, while the remaining; id(record id), createdOn(time of reporting) and status(initially as draft) are system generated
 
2. Get all red flags:
URL: GET/api/v1/red_flags
This fetches and returns an array of all records along if any record(S) else response message informing of the absence of any records

3. Get individual record:
URL: GET/api/v1/red_flags/<id>
With an integer id of an existing record, fetches and returns the given record, else returns appropriate error message
  
4. Edit a given record;
URL: PATCH/api/v1/red_flags/<id>/<attribute>
Edits the record specified attribute of the record with the given id. The editable attributes include comment, location and status.
Editing the status and comment of a record will replace current values with the supplied values while updating the location ill append geolocation coordinated to the physical address given during creation of the record. The location value fore edit must be a string containing only the latitude and longitude respectively separated by a single space, else a corresponding error response will be returned.
  
5. Delete a given record:
URL: DELETE/api/v1/red_flags/<id>/delete
If record with given id exists, request will delete the record and return a 'record deleted' message in the response, else it will return record not  found message
  
6. Usage info:
URL: GET/api/v1/
This base(default) root displays a simple user guide

ERROR HANDLING
Errors are either in the request body(input data) or URL. The application does not assume values and attempt to correct errors but will identify the cause of each error and send a response with possible causes: Examples are:
No body for post/patch request, response: empty request
Empty or misspelled input attribute key for post/patch request, response: missing key for <attribute>, please check attribute or spelling
Missing value for a mandatory attribute to a given post/patch request, response: missing <attribute> key
Resource specified for operation non-existent, response: record unavailable
Attempt to edit unauthorized attribute, response: <attribute> cannot be edited
There is also a similar set of errors for URL errors
In the event of multiple errors in a single request, the response will give the first error caught and subsequently display next error when the present has been cleared(subsequent requests). Example: Say an edit request specified an un-editable attribute as target for a non existent record and the attribute name was miss spelled in the request body, the responses in order on subsequent execution of the request after making the necessary correction will be missing key for <attribute>, <attribute> can not be edited and record not available

ACCESS:
This product can be accessed through the cloud hosting link provided in the links and related information section

TECHNOLOGIES USED

Python language
Flask framework

ACKNOWLEDGEMENTS: A great deal of indebtedness to Andela uganda for providing not only an opportunity to explore and exploit talent, but also the environment, resources and narturing

A lot of contribution and mentoring from the learning facilaitators at the Andela Levelup program is plainly unequaled in the realization of this product to this stage, especially the patience and understanding the facilitators unceasingly exercised

PRODUCT LINKS AND RELATED INFORMATION

Code: https://github.com/Anguandia/i-reporter
Cloud hosting: https://agile-basin-53232.herokuapp.com/
Pivotal tracker: https://www.pivotaltracker.com/n/projects/2232384 Contains the project plan, implementation and management details
Documentation: https://app.swaggerhub.com/apis/Anguandia/iReporter/1# Technical documentation of application detailing usage, parameters, expected behavior, requests and responses, etc 
Licencing: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
