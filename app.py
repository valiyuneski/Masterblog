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


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    with open("blog_posts.json", "r") as f:
        blog_posts = json.load(f)

    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if request.method == "POST":
        if post:
            blog_posts = [p for p in blog_posts if p["id"] != post_id]
            with open("blog_posts.json", "w") as f:
                json.dump(blog_posts, f, indent=2)
        return redirect(url_for("index"))

    return render_template("delete.html", post=post)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    fetch_post_by_id_lambda = lambda post_id: next(
        (p for p in json.load(open("blog_posts.json", "r")) if p["id"] == post_id), 
        None
    )

    post = fetch_post_by_id_lambda(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == 'POST':
        # Update the post in the JSON file
        # Load all posts
        with open("blog_posts.json", "r") as f:
            blog_posts = json.load(f)

        # Find the post to update
        for p in blog_posts:
            if p["id"] == post_id:
                p["title"] = request.form["title"]
                p["author"] = request.form["author"]
                p["content"] = request.form["content"]
                break

        # Save updated posts back to JSON file
        with open("blog_posts.json", "w") as f:
            json.dump(blog_posts, f, indent=2)
            
        # Redirect back to index
        return redirect(url_for("index"))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)