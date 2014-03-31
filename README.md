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

obid, source location, mimetype, blob

Metadata:
---------

obid, metadataid, json-blob

metadataid, Human readable description
