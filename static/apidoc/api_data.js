define({ "api": [
  {
    "type": "get",
    "url": "/api/getMusic",
    "title": "Get song data",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "artist",
            "description": "<p>The exact song's artist name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "album",
            "description": "<p>The exact song's album name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "title",
            "description": "<p>The exact song's title on the system.</p> "
          }
        ]
      }
    },
    "description": "<p>API getMusic route makes a GET to get the Music from the DB, Returns JSON object.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "group": "D__DevProjects_GitHub_MoodMusic_server_py",
    "groupTitle": "D__DevProjects_GitHub_MoodMusic_server_py",
    "name": "GetApiGetmusic",
    "sampleRequest": [
      {
        "url": "https://localhost:5000/api/getMusic"
      }
    ]
  },
  {
    "type": "post",
    "url": "/api/humeur",
    "title": "Post song mood",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "artist",
            "description": "<p>The exact song's artist name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "album",
            "description": "<p>The exact song's album name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "title",
            "description": "<p>The exact song's title on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "humeur",
            "description": "<p>The mood classification given to the song. TODO, enumerate the moods.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "email",
            "description": "<p>TODO, The email of the user that post the mood classfication.</p> "
          }
        ]
      }
    },
    "description": "<p>Route to post a mood to song.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "group": "D__DevProjects_GitHub_MoodMusic_server_py",
    "groupTitle": "D__DevProjects_GitHub_MoodMusic_server_py",
    "name": "PostApiHumeur",
    "sampleRequest": [
      {
        "url": "https://localhost:5000/api/humeur"
      }
    ]
  },
  {
    "type": "post",
    "url": "/api/note",
    "title": "Post a song rate",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "artist",
            "description": "<p>The exact song's artist name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "album",
            "description": "<p>The exact song's album name on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "title",
            "description": "<p>The exact song's title on the system.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>number</p> ",
            "size": "1",
            "allowedValues": [
              "1",
              "2",
              "3",
              "4",
              "5"
            ],
            "optional": false,
            "field": "note",
            "description": "<p>The rating given to the song.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "email",
            "description": "<p>TODO, The email of the user that post the rating.</p> "
          }
        ]
      }
    },
    "description": "<p>API note to set a note for a song. Returns JSON object.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "group": "D__DevProjects_GitHub_MoodMusic_server_py",
    "groupTitle": "D__DevProjects_GitHub_MoodMusic_server_py",
    "name": "PostApiNote",
    "sampleRequest": [
      {
        "url": "https://localhost:5000/api/note"
      }
    ]
  }
] });