# Local set up (Mac):

Ensure you have postgres setup

[ Will add a dump in the future, for now follow: https://gist.github.com/rchakra3/859ac29645078f4ba9a9 ]

```
virtualenv env

source env/bin/activate

pip install -r requirements.txt
```

# Run the server:

```
python aye/run.py
```

# Using the API:

## INSERT
    Send Post requests of mime type: application/json to:
    
    localhost:9000/new_event

    with fields: 'event_name', 'event_description', 'longitude', 'latitude'

## LOOKUP
    Send Post requests of mime type: application/json to:

    localhost:9000/find_event

    with fields: 'longitude', 'latitude', 'distance'
