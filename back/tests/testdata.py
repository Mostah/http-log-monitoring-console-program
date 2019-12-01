from ..log_pipeline.metrics import SectionMetrics
from datetime import datetime

test_statistics_data = {
    "batch": [
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573860,
            "request": "GET /api/user HTTP/1.0",
            "status": 404,
            "bytes": 1234
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573861,
            "request": "GET /api/help HTTP/1.0",
            "status": 200,
            "bytes": 965
        },
        {
            "remotehost": "10.0.0.3",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573862,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1234
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573863,
            "request": "POST /api/user HTTP/1.0",
            "status": 401,
            "bytes": 1203
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573864,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
        }
    ],
    "hits": [
        {
            'number': 5,
            'time' : ''
        },
        {
            'number': 12,
            'time' : ''
        },
        {
            'number': 3,
            'time' : ''
        },
        {
            'number': 1,
            'time' : ''
        }
    ],
    "metrics_batch": [
        SectionMetrics('api','',12,0,0,0,0,''),
        SectionMetrics('api','',2,0,0,0,0,''),
        SectionMetrics('api','',14,0,0,0,0,''),
        SectionMetrics('api','',28,0,0,0,0,''),
        SectionMetrics('api','',0,0,0,0,0,''),
    ]
} 

test_statistics_manager_data = {
    "logs": [
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573864,
            "request": "GET /api/user HTTP/1.0",
            "status": 200,
            "bytes": 1307
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573864,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1549573864,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1307
        }
    ],
    "general_batch": [{
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281726612,
            "request": "GET /api/user HTTP/1.0",
            "status": 404,
            "bytes": 1234
        },
        {
            "remotehost": "10.0.0.4",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730201,
            "request": "GET /api/help HTTP/1.0",
            "status": 200,
            "bytes": 965
        },
        {
            "remotehost": "10.0.0.3",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730211,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1234
        },
        {
            "remotehost": "10.0.0.5",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730211,
            "request": "POST /api/user HTTP/1.0",
            "status": 401,
            "bytes": 1203
        },
        {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730211,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
        }],
    "section_batch": {
        'api':[
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281726612,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
            },
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730211,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
            },
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281730211,
            "request": "GET /api HTTP/1.0",
            "status": 200,
            "bytes": 1307
            }
        ],
        'report': [
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281726612,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1307
            },
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281726612,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1307
            },
            {
            "remotehost": "10.0.0.2",
            "rfc931": "-",
            "authuser": "apache",
            "date": 1281726612,
            "request": "GET /report HTTP/1.0",
            "status": 200,
            "bytes": 1307
            }
        ]
    },
    "general_hits": [
        {
            'number': 5,
            'time' : datetime(2010,8,13,22,10,11)
        },
        {
            'number': 12,
            'time' : datetime(2010,8,13,22,8,11)
        },
        {
            'number': 3,
            'time' : datetime(2010,8,13,21,10,12)
        },
        {
            'number': 1,
            'time' : datetime(2010,8,13,21,10,12)
        }
    ],
    "section_hits": {
        'api': [
            {
                'number': 5,
                'time' : datetime(2010,8,13,22,10,11)
            },
            {
                'number': 12,
                'time' : datetime(2010,8,13,22,8,11)
            },
            {
                'number': 3,
                'time' : datetime(2010,8,13,22,8,11)
            },
            {
                'number': 1,
                'time' : datetime(2010,8,13,21,10,12)
            }
        ],
        'report': [
            {
                'number': 5,
                'time' : datetime(2010,8,13,22,10,11)
            },
            {
                'number': 12,
                'time' : datetime(2010,8,13,21,10,12)
            },
            {
                'number': 3,
                'time' : datetime(2010,8,13,21,10,12)
            },
            {
                'number': 1,
                'time' : datetime(2010,8,13,21,10,12)
            }
        ]
    },
}

test_alerter_data = {
    "section_metrics": {
        'api': [
            SectionMetrics('api',datetime(2010,8,13,22,9,8),12,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,22,9,12),16,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,22,8,50),8,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,21,10,12),11,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,21,10,12),13,0,0,0,0,''),
        ],
        'report': [
            SectionMetrics('api',datetime(2010,8,13,22,9,8),9,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,22,9,12),11,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,22,8,50),7,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,22,8,40),2,0,0,0,0,''),
            SectionMetrics('api',datetime(2010,8,13,21,10,12),9,0,0,0,0,''),
        ],
        'user': [
            SectionMetrics('user',datetime(2010,8,13,22,9,8),10,0,0,0,0,''),
            SectionMetrics('user',datetime(2010,8,13,22,9,12),11,0,0,0,0,''),
            SectionMetrics('user',datetime(2010,8,13,22,8,50),9,0,0,0,0,''),
            SectionMetrics('user',datetime(2010,8,13,22,8,40),10,0,0,0,0,''),
            SectionMetrics('user',datetime(2010,8,13,21,10,12),1,0,0,0,0,''),
        ]
    },
    "sections_metrics_to_push": {
        'api': SectionMetrics('api',datetime(2010,8,13,22,9,8),12,0,0,0,0,''),
        'report': SectionMetrics('api',datetime(2010,8,13,22,9,8),4,0,0,0,0,''),
        'user': SectionMetrics('user',datetime(2010,8,13,22,9,8),10,0,0,0,0,'')
    }
}