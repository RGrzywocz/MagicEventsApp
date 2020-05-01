from flask import Flask, jsonify, request, render_template
import datetime
import random

app = Flask(__name__)
# all the events stored in the list - 2 examples included
events = [{'title': 'Event example - Hackathon',
           'start_date': datetime.datetime(2020, 5, 3),
           'end_date': datetime.datetime(2020, 5, 7),
           'thumbnail': 'https://cloudfour.com/examples/img-currentsrc/images/kitten-small.png',
           'participants': [{'name': 'Adam',
                             'reservation_code': '1234567890'
                             },
                            {'name': 'John',
                             'reservation_code': '9999911111'}],
           'booking_open': True
           },
          {'title': 'Event example - football',
           'start_date': datetime.datetime(2020, 5, 8),
           'end_date': datetime.datetime(2020, 5, 8),
           'thumbnail': 'https://pngimage.net/wp-content/uploads/2018/06/small-ball-png-.png',
           'participants': [{'name': 'footbal fan1',
                             'reservation_code': '1232567890'
                             },
                            {'name': 'foorbal fan2',
                             'reservation_code': '9929911111'}],
            'booking_open': True
           },
          ]


@app.route('/')
def hello_world():
    return render_template('event.html', events=events)


# POST - user apply for event /<string:event_title>/apply {name:}
@app.route('/<string:event_title>/apply', methods=['POST'])
def apply_for_event(event_title):
    request_data = request.get_json()
    reservation_code = str(random.randint(1000000000, 9999999999))
    new_participant = {'name': request_data['name'],
                       'reservation_code': reservation_code}
    for event in events:
        if event['title'] == event_title:
            if event['booking_open']:
                event['participants'].append(new_participant)
                return jsonify({'message': 'Your application for event ' + event_title + ' was succesfull.',
                               'reservation_code': reservation_code})
            return jsonify({'message': 'Booking is closed'})
    return jsonify({'message': 'Event was not found in database, try again'})


# DELETE - management cancel event /admin/<string:event_title>/cancel_event
@app.route('/admin/<string:event_title>/cancel_event', methods=['DELETE'])
def cancel_event(event_title):
    for event in events:
        if event_title == event['title']:
            if abs((event['start_date'] - datetime.datetime.now()).days) > 2:
                events.remove(event)
                return jsonify({'events': event['title'] for event in events})
            else:
                return jsonify({'events': [event['title'] for event in events],
                                'message': 'Its too late to cancel  event(less then 2 days)'})
    return jsonify({'events': [event['title'] for event in events],
                    'message': 'Event not found'})


# DELETE - management deletes participant from event
# /admin/<string:event_title>/delete_participant/<string:reservation_code>
@app.route('/admin/<string:event_title>/delete_participant/<string:reservation_code>', methods=['DELETE'])
def delete_participant(event_title, reservation_code):
    for event in events:
        if event_title == event['title']:
            for participant in event['participants']:
                if participant['reservation_code'] == reservation_code:
                    event['participants'].remove(participant)
                    return jsonify({'participants': event['participants']})
            return jsonify({'participants': event['participants'],
                            'message': 'participant not found'})
    return jsonify({'events': [event['title'] for event in events],
                    'message': 'event not found'})


# POST - management adds new event /admin/add_event {title:, start_date:, end_date:, thumbnail:}
@app.route('/admin/add_event', methods=['POST'])
def add_event():
    request_data = request.get_json()
    new_event = {'title': request_data['title'],
                 'start_date': request_data['start_date'],
                 'end_date': request_data['end_date'],
                 'thumbnail': request_data['thumbnail'],
                 'participants': []}
    events.append(new_event)
    return jsonify(new_event)


# POST - management can stop booking /admin/<string:event_title>/stop_booking
@app.route('/admin/<string:event_title>/stop_booking', methods=['POST'])
def stop_booking(event_title):
    for event in events:
        if event['title'] == event_title:
            if abs((event['start_date'] - datetime.datetime.now()).days) > 2:
                event['booking_open'] == False
                return jsonify({'event': event})
            else:
                return jsonify({'event': event, 'message': 'too late to stop booking'})
    return jsonify({'events': events, 'message': 'event not found'})


# POST - user cancels attendance for event /<string:event_title>/cancel/<string:reservation_code>
@app.route('/<string:event_title>/cancel/<string:reservation_code>', methods=['DELETE'])
def cancel_attendance(event_title, reservation_code):
    for event in events:
        if event['title'] == event_title:
            for participant in event['participants']:
                if participant['reservation_code'] == reservation_code:
                    event['participants'].remove(participant)
                    return jsonify({'message': 'You have been removed from event'})
                return jsonify({'message': 'Yours code wasnt found'})
    return jsonify({'message': 'event not found'})


app.run()
