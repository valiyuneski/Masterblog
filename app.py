from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts() -> list:
    """Load blog posts from the JSON file."""
    try:
        with open("blog_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: blog_posts.json not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON - {e}")
        return []


def save_blog_posts(blog_posts, filename="blog_posts.json") -> bool:
    """Save blog posts to a JSON file safely."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(blog_posts, f, indent=2, ensure_ascii=False)
        return True
    except (OSError, TypeError) as e:
        print(f"Error saving {filename}: {e}")
        return False


@app.route("/")
def index():
    """Home page that lists all blog posts."""
    blog_posts = load_blog_posts()

    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        # Load existing blog posts
        blog_posts = load_blog_posts()

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
        save_blog_posts(blog_posts)

        # Redirect back to home page
        return redirect(url_for('index'))

    # GET request just renders the form
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=['GET', 'POST'])
def delete(post_id):
    """ GET switches only to 'delete.html', and POST does the delete itself"""
    if request.method == 'POST':
        """Delete a blog post by ID."""
        blog_posts = load_blog_posts()
        post_to_delete = next((p for p in blog_posts if p.get("id") == post_id), None)
        if post_to_delete is None:
            return "Post not found", 404
    
        # Remove the post from the list
        blog_posts = [p for p in blog_posts if p.get("id") != post_id]

        # Save back to JSON
        save_blog_posts(blog_posts)
        return redirect(url_for("index"))
    
    # First Navigation is: GET request (so that DELETE.HTML is shown)
    return render_template('delete.html', post=post_to_delete)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update a blog post by ID."""
    blog_posts = load_blog_posts()
    post = next((p for p in blog_posts if p.get("id") == post_id), None)
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        # Find the post to update
        for p in blog_posts:
            if p["id"] == post_id:
                p["title"] = request.form["title"]
                p["author"] = request.form["author"]
                p["content"] = request.form["content"]
                break

        # Save updated posts back to JSON file
        save_blog_posts(blog_posts)
            
        # Redirect back to index
        return redirect(url_for("index"))

    # First Navigation is: GET request (update, all fileds are editable for changes ...)
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)