from flask import Flask, request, jsonify,render_template
app=Flask(__name__)

@app.route('/shop')
def home():
    return render_template('malefashion-master/shop.html')



@app.route('/product')
def product():
    return render_template('malefashion-master/shop-details.html')
app.run(debug=True)