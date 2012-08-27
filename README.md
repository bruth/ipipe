# Pipe

Pipe is a tiny library for making simple processing pipelines. To keep things
simple and generic, it assumes and takes advantage of Python's [iterator
protocol][1], allowing each component to feed into the next. This allows
for interfacing with built-in container types, files, database cursors, etc.

[ETL][2] can be a painstaking task and dealing with sometimes wildly
different data files or formats can result in inconsistent, hacked together
scripts that are difficult to maintain and opaque to other developers.

Pipe supports a few built-in functions for performing common tasks sorting
data and merging ordered sets of data.

[1]: http://docs.python.org/library/stdtypes.html#iterator-types
[2]: http://en.wikipedia.org/wiki/Extract,_transform,_load

## Idea Scratchpad

### Integration of Sources

- define common variables
- define distribution key(s) for binning
- define mapping between raw source format to target format
    - indicies to keys, etc.
- flow of etl
    - read data
    - parse into data structure
        - array/dict
    - transform parsed data structure into intended format and types
    - calculate or derive necessary values from parsed and cleaned data
    - sort by distribution key(s) for binning
    - partition each data source into bins for parallel processing
    - distribute sources into their respective bins
    - perform the combining step on each bin
        - combine data into a single object
    - combine result from each bin
    - load cleaned, populated data into target

### File Composition

- Surrogate keys are managed locally and do not change
    - They are effectively a non-natural _key_ that is being treated as a such
- Keeps track of changes over time as new versions of data are made available
    - The new data file is sorted the same way as the identity file so lines
    can be compared
- Process Flow
    - Lines are being read one at a time from the input file
    - Check if the line identity matches via the identity comparison
        - If so, compare the contents of the input line
            - If it does not match, add it to the `updates` list
    - If the line does not match
        - Compare the lexicographical ordering of the key
            - If it is less than the current ident line, add it to the
            `inserts` list
            - If it is greater than the current line, add the ident id to
            the `deletes` list (for logging purposes)


## Example

```python
from pipe import FileParser, Parser, FileReader, CursorReader, Sorter, compose

# Create a file reader which takes a file handler and a file parser. This
# will produce an iterable that emits a line per iteration (note the file
# file object behaves this way already).
freader = FileReader(open('data.txt'))

# Create a file parser that understands general properties about text files
# to enable parsing. This includes column delimiters, skipping lines, etc.
fparser = FileParser(freader, delimiter='\t', skiplines=1)

# Define a producer which takes a reader and specifies a list of field names
# corresponding to those emitted from the reader.
fprod = Producer(fparser, ['first_name', 'last_name', 'dob', 'twitter', 'email'])

# The producer can be iterated over producing a convenient namedtuple record.
# for record in fileprod:
#     print '{} {} ({})'.format(record.first_name, record.last_name, record.twitter)


# `parse_N` methods can be defined on Parser subclasses to handle a particular
# position. If a list or tuple is returned, it will be extended to the output
# row rather than appended. Override `parse` to parse the entire row. 
class RowParser(Parser):
    def parse_0(self, value):
        # Parse the full name into separate parts..
        return value.split()

creader = CursorReader(cursor)
cparser = RowParser(creader)

# Same deal as above.. the fields are in a different order than above
cprod = Producer(cparser, ['first_name', 'last_name', 'email', 'dob', 'gplus'])

# Let's merge them together to compose a single record per unique record. First
# create an identity function that takes a record and returns it's _identity_.
# `compose` requires all input iterables to be ordered relative to the fields
# use in the identity function.
def identity(record):
    return record.first_name, record.last_name, record.dob, record.email

# Use the same function to sort each producer
fsorted = Sorter(fprod, key=identity)
csorted = Sorter(cprod, key=identity)

for record in compose(fsorted, csorted, identity=identity):
    # Will contain the identity info as well as the twitter and google plus
    # usernames for a given person.
    print record
```
