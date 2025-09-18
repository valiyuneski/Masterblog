from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("blog_posts.json", "r") as f:
        blog_posts = json.load(f)
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        # Load existing blog posts
        with open('blog_posts.json', 'r') as f:
            blog_posts = json.load(f)

        # Generate new ID (max existing ID + 1)
        new_id = max([post['id'] for post in blog_posts], default=0) + 1

        # Create new post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append and save back to JSON
        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f, indent=2)

        # Redirect back to home page
        return redirect(url_for('index'))

    # GET request just renders the form
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)