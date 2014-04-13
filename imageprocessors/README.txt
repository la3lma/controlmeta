In this directory we're developing a very simple image processing
example that uses the controlmeta infrastructure to do its work.

Architecturally it's an actor architecture that looks for incoming
messages in the form of "tasks" placed in the controlmeta storage.

The tasks are image processing tasks. Basically this is what
we do:

 o Listen for incoming images.
 o When an image arrives, create tasks to look for faces in them.
 o Set up face recognition actors that are activated once faces
   become available for them to process.
 o The face recognition actors consume face recogntion tasks by
   picking up the pictures, running a Haar classifier over them
   and detecting squares where faces are.  These faces are then
   extracted and stored as images in the controlmeta storage with
   links to the original image.
 o Initially we could just assume that the processing agents just
   poll periodically and pick up tasks of a kind they are able to
   process.  This clearly isn't very scalable for a variety of 
   reasons, so at some stage we'll have to think about
   some way to distribute intents to a possibly large(ish)
   amount of agents.  0MQ seems to be a possibility there, but
   we'll see eventually what turns out to be the best option.


