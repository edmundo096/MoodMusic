define({ "api": [
  {
    "type": "get",
    "url": "/api/getMusic",
    "title": "Get song data",
    "name": "api_get_music",
    "group": "Song",
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
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "artist",
            "description": "<p>The song artist name on the system.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "album",
            "description": "<p>The song album name on the system.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "title",
            "description": "<p>The song title on the system.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "year",
            "description": "<p>The song year of release on the system.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "label",
            "description": "<p>The song label on the system.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "music_path",
            "description": "<p>The song's YouTube video ID.</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "image_path",
            "description": "<p>The song cover image URL (currently not used).</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response for an example song:",
          "content": "{\n    \"album\":\"Motion\",\n    \"artist\":\"Calvin Harris\",\n    \"image_path\":null,\n    \"label\":\"Columbia Records; Syco; Syco Music UK\",\n    \"music_path\":\"ebXbLfLACGM\",\n    \"title\":\"Summer\",\n    \"year\":2014\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "<p>number</p> ",
            "optional": false,
            "field": "result",
            "description": "<p>The result of the GET, being <code>-1</code> for incomplete/incorrect parameters, or <code>0</code> for a song not found.</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "{ \"result\": 0 }",
          "type": "json"
        }
      ]
    },
    "description": "<p>API getMusic route makes a GET to get the Music from the DB. Returns JSON object.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "groupTitle": "Song",
    "sampleRequest": [
      {
        "url": "http://moodmusic-ltu.herokuapp.com/api/getMusic"
      }
    ]
  },
  {
    "type": "post",
    "url": "/api/mood",
    "title": "Post song mood",
    "name": "api_post_mood",
    "group": "Song",
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
            "allowedValues": [
              "Chill",
              "Sad",
              "Nostalgic",
              "Gaming",
              "Travel",
              "Motivated",
              "Enthusiastic",
              "Upset",
              "Inspired",
              "Festive",
              "Hard",
              "Geek",
              "Instrumental",
              "Creative",
              "Tropical",
              "Studious",
              "Aggressive",
              "Calm",
              "Adventurous",
              "Humorous"
            ],
            "optional": false,
            "field": "mood",
            "description": "<p>The mood classification given to the song.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "email",
            "description": "<p>The email of the user that post the mood classification. Note: If a valid cookie that identifies an user is sent, then this parameter is optional.</p> "
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>number</p> ",
            "optional": false,
            "field": "result",
            "description": "<p>The result of the POST, being <code>1</code> for Success.</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{ \"result\": 1 }",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "<p>number</p> ",
            "optional": false,
            "field": "result",
            "description": "<p>The result of the POST, being <code>-1</code> for incomplete/incorrect parameters, or <code>0</code> for a song not found.</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "{ \"result\": 0 }",
          "type": "json"
        }
      ]
    },
    "description": "<p>Route to post a mood to song.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "groupTitle": "Song",
    "sampleRequest": [
      {
        "url": "http://moodmusic-ltu.herokuapp.com/api/mood"
      }
    ]
  },
  {
    "type": "post",
    "url": "/api/rating",
    "title": "Post a song rating",
    "name": "api_post_rating",
    "group": "Song",
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
            "field": "rating",
            "description": "<p>The rating given to the song.</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>string</p> ",
            "optional": false,
            "field": "email",
            "description": "<p>The email of the user that post the rating. Note: If a valid cookie that identifies an user is sent, then this parameter is optional.</p> "
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>number</p> ",
            "optional": false,
            "field": "result",
            "description": "<p>The result of the POST, being the sent Rating from <code>1</code> to <code>5</code> for Success.</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response for a 4 start Rating:",
          "content": "{ \"result\": 4 }",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "<p>number</p> ",
            "optional": false,
            "field": "result",
            "description": "<p>The result of the POST, being <code>-1</code> for incomplete/incorrect parameters, or <code>0</code> for a song not found.</p> "
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "{ \"result\": 0 }",
          "type": "json"
        }
      ]
    },
    "description": "<p>API note to set a note for a song. Returns JSON object.</p> ",
    "version": "0.0.0",
    "filename": "./server.py",
    "groupTitle": "Song",
    "sampleRequest": [
      {
        "url": "http://moodmusic-ltu.herokuapp.com/api/rating"
      }
    ]
  }
] });