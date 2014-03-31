controlmeta
===========

The overall idea is to have a repository for image data and metadata
about the images.  The image data is pretty simple, just a blob of
image data and a mime type to decode it.  The metadata is a bit more
complex.  There are many kinds of metadata we can imagine: Faces,
faces associated with names.  Wall clocks, cars, cigarettes, boats,
meetings, relationships between people. etc.  The only thing that can
be said about the metadata is that it is incredibly diverse.   So an
initial challenge will be how to represent it all. Here is a sketch
foo how we can go about that.

Persistent data model
=====================

We model the whole thing in postgresql using a hybrid relational /
Json(nosql) model.

Raw data:
--------

obid, source uri, mimetype, blob

The obid is an unique object id. The source uri is an URI (or
equivalent) that points to the location where the data can unuquely be
found.  The blob is just the bytes of the object and the mimetype
describes it.

So far so good.  We will also allow, but not encourage, that the blob
is empty.  In that case the semantics should be to look up the source
and get the bytes from there.  This allows us to work with skinny
databases in situations where that is useful (like testing perhaps).
It is not encouraged for production use.

Metadata:
---------

obid, metadataid, json-blob

metadataid, Human readable description

Inherent in this model there is the possibility of the json blobs
having a high number of foreign keys into external data models,
e.g. people (identities), various ontologies for this that or the
other thing.   We chose simply to say: Good for them.  There will
be room for consolidation, but this model simply will not care.


Task distribution
=================

This will have to be a distributed model.  The metadata annotation
agents should get a task from somewhere, get the raw data and perhaps
other metadata it requires, perform a calculation and then write the
result to the metadata repo.

IT IS CRUCIAL THAT THIS MODEL IS IN PLACE FROM DAY ONE!

This is the one thing that we can't compromise on when it comes
to scaling.

It _must_ be possible to write small scripts in whatever to do 
things.  These scripts should be first class citizens in the 
ingestion facility.

Distribution of tasks should use some queueing mechanism.  Either one
from amazon or perhaps 0MQ.

The tasks are then picked up, processed and the results stored back to
the metadata storage.  It can then be used for search & collation by known
features ("tags").


REST interface
=============

The task distribution network will have a REST interface so that it's
possible to read/write all data from/to the central service.  Agents
should only have to communicate through REST, and optionally through
whatever methods are used to access actual content (e.g. direct access
to S3, or a filesystem or whatever).


Accessing media and metadata
----------------------------

GET /media/id/{id}/media
 -> Gets the content stored in the blob

PUT /media/id/{id}/media
 -> Upload new media, get an ID back in the reply.

GET /media/id/{id}/meta/{metatype}
 -> The JSON describing the metadata

PUT /media/id/{id}/meta/{metatype}
 -> The JSON describing the metadata


Accessing the task queue
------------------------

Some ideas:
------

Creating and updating individual tasks
.....

GET /task/id/{id}
PUT /task/id/{id}

GET /task/{type/{type}}/waiting/next
GET /task/{type/{type}}/waiting/pick
GET /task/{type/{type}}/in-progress/list
GET /task/{type/{type}}/done/list
GET /task/{type/{type}}/list







