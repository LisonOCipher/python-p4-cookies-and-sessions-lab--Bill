#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Check if 'page_views' exists in the session, if not, set it to 0
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the page_views by 1
    session['page_views'] += 1
    
    # Check if page_views is greater than 3
    if session['page_views'] < 3:
        # Return article data in JSON response
        article = Article.query.get(id)
        if article:
            return jsonify({
                'id': article.id,
                'title': article.title,
                'author': article.author,
                'content': article.content,
                'preview': article.content[:50],  # Adding a preview of the content
                'minutes_to_read': article.minutes_to_read  # Adding minutes_to_read
            }), 200
        else:
            return jsonify({'message': 'Article not found'}), 404
    else:
        # Return error message and 401 status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
