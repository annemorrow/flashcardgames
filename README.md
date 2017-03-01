# FlashCard Games

## Backend

A CRUD app where users can make lists and then fill lists with question and answer pairs.  Lists belong to users, and questions belong to lists.  At this time, questions are expected to belong to a single list and lists to a single user.  However, I intend to make it easy to download/upload csv files so that many questions can be added at once, and I intend that users should be able to move questions between lists.

## Frontend

Different games which use question lists.  These games might include jeopardy, timed flashcards, etc.

## Wishlist

* upload and download question lists as csv files (so teachers don't fear loosing their lists and can use lists easily in other contexts)
    * problem: differentiate between uploading csv files that are meant to replace a list (if a question isn't on the file, it's no longer in the list) and csv files that are meant to add to a list (all questions are considered to be new and the questions already in the list remain unchanged)
* create custom randomized printable quizes/tests based on lists
* facilitate multiple choice and true/false questions as well as short answer
* create sharable urls so that teachers can let students practice on a list without giving them full editorial control
