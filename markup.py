

def header(backgroundcolor,textcolor,name, cart):
    str=''
    for row in selectAll("Menu"):
        url=url_for(row['link'])
        str=str+"""<li><a href='"""+url+"""' style="color:"""+textcolor+""";">"""+row['Label']+"""</a></li>"""
    return """<div class="site-navbar bg-white py-2" >
  <div class="search-wrap">
    <div class="container">
      <a href="#" class="search-close js-search-close"><span class="icon-close2"></span></a>
      <form action="#" method="post">
        <input type="text" class="form-control" placeholder="Search keyword and hit enter...">
      </form>
    </div>
  </div>
  <div class="container" style="background-color:"""+backgroundcolor+""";">
    <div class="d-flex align-items-center justify-content-between">
      <div class="logo">
        <div class="site-logo">
          <a href="index.html" class="js-logo-clone" style="color:"""+textcolor+""";">"""+name+"""</a>
        </div>
      </div>
      <div class="main-nav d-none d-lg-block">
        <nav class="site-navigation text-right text-md-center" role="navigation">
          <ul class="site-menu js-clone-nav d-none d-lg-block">
          """+str+"""
          </ul>
        </nav>
      </div>
      <div class="icons">
        <a href="#" style="color:"""+textcolor+""";" class="icons-btn d-inline-block js-search-open"><span class="icon-search"></span></a>
        <a href="cart.html" style="color:"""+textcolor+""";"class="icons-btn d-inline-block bag">
          <span class="icon-shopping-bag"></span>
          <span class="number">"""+cart+"""</span>
        </a>
        <a href="#" class="site-menu-toggle js-menu-toggle ml-3 d-inline-block d-lg-none"><span class="icon-menu"></span></a>
      </div>
    </div>
  </div>
</div>"""


def card1(backgroundcolor,textcolor,title,tagline,price,link,image):
    return """<div class="site-blocks-cover" data-aos="fade" style="background-color:"""+backgroundcolor+""";">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-5 text-center">
        <div class="featured-hero-product w-100">
          <h1 class="mb-2" style="color:"""+textcolor+""";">"""+title+"""</h1>
          <h4 style="color:"""+textcolor+""";">"""+tagline+"""</h4>
          <div class="price mt-3 mb-5" style="color:"""+textcolor+""";"><strong>$"""+price+"""</strong></div>
          <p><a href="/shop.html" class="btn btn-outline-primary rounded-0">Shop Now</a> <a href='"""+link+"""' class="btn btn-primary rounded-0">Buy Now</a></p>
        </div>
      </div>
      <div class="col-lg-7 align-self-end text-center text-lg-right">
        <img src='"""+image+"""' alt="Image" class="img-fluid img-1">
      </div>
    </div>
  </div>
</div>"""

def card2(backgroundcolor,textcolor,hashtag,title,link,image):
    return """<div class="site-blocks-cover inner-page py-5"  data-aos="fade" style="background-color:"""+backgroundcolor+""";">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-6 ml-auto order-lg-2 align-self-start">
        <div class="site-block-cover-content">
        <h2 class="sub-title" style="color:"""+textcolor+""";">#"""+hashtag+"""</h2>
        <h1 style="color:"""+textcolor+""";">"""+title+"""</h1>
        <p><a href='"""+link+"""' class="btn btn-black rounded-0">Shop Now</a></p>
        </div>
      </div>
      <div class="col-lg-6 order-1 align-self-end">
        <img src='"""+image+"""' alt="Image" class="img-fluid">
      </div>
    </div>
  </div>
</div>"""

def carousel(rows,title):
    str=''

    for row in rows:
        p = format(row['Price'], '.2f')
        url=url_for('shopsingle',prod=row['Name'])
        str=str+"""<div class="product">
        <a href='"""+url+"""' class="item">
          <img alt="Embedded Image" src='"""+row['Image']+"""' class="center"/>
          <div class="item-info">
            <h3 style="text-align:center">"""+row['Name']+"""</h3>
            <h5 class="price" style="text-align:center">$"""+p+"""</h5>
            </div>
            </a>
            </div>"""
    return """<div class="site-section">
              <div class="container">
                <div class="row">
                  <div class="title-section text-center col-12">
                    <h2 class="text-uppercase">"""+title+"""</h2>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 block-3 products-wrap">
                    <div class="nonloop-block-3 owl-carousel">
                        """+str+"""
                    </div>
                  </div>
                </div>
              </div>
            </div>"""

def carousel2(rows,title):
    str=''
    for row in rows:
        url=url_for('artist',art=row['Name'])
        str=str+"""<div class="product">
          <a href='"""+url+"""' class="item">
            <img alt="Embedded Image" src='"""+row['Image']+"""'"/>
            <div class="item-info">
              <h3>"""+row['Name']+"""</h3>
            </div>
          </a>
        </div>"""
    return """<div class="site-section">
            <div class="container">
            <div class="row">
              <div class="title-section text-center col-12">
                <h1 class="text-uppercase">"""+title+"""</h1>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12 block-3 products-wrap">
                <div class="nonloop-block-3 owl-carousel">
                  """+str+"""
                </div>
              </div>
            </div>
            </div>
            </div>"""

def footer(backgroundcolor,textcolor,about,address,phonenumber,email, subsciber_form):
    return """<footer class="site-footer custom-border-top">
  <div class="container" style="background-color:"""+backgroundcolor+""";">
    <div class="row">
      <div class="col-md-6 col-lg-3 mb-4 mb-lg-0">

        <div class="block-7">
          <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">About Us</h3>
          <p style="color:"""+textcolor+""";">"""+about+"""</p>
        </div>
        <div class="block-7">
          <form action="{{url_for('subscribed')}}" method='post'>
            {{ subsciber_form.csrf_token }}
            <label for="email_subscribe" class="footer-heading" style="color:"""+textcolor+""";">Subscribe</label>
            <div class="form-group">
            {{ subsciber_form.email(class="form-control py-4", placeholder="Email") }}
              <input type="submit" class="btn btn-sm btn-primary" value="Send">
            </div>
          </form>
        </div>
      </div>
      <div class="col-lg-5 ml-auto mb-5 mb-lg-0">
        <div class="row">
          <div class="col-md-12">
            <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">Quick Links</h3>
          </div>
          <div class="col-md-6 col-lg-6">
            <ul class="list-unstyled">
              <li><a href="/index.html" style="color:"""+textcolor+""";">Home</a></li>
              <li><a href="/shop.html" style="color:"""+textcolor+""";">Products</a></li>
              <li><a href="/shopservices.html" style="color:"""+textcolor+""";">Services</a></li>
              <li><a href="/cart.html" style="color:"""+textcolor+""";">Shopping cart</a></li>
              <li><a href="/contact.html" style="color:"""+textcolor+""";">Contact</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="block-5 mb-5">
          <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">Contact Info</h3>
          <ul class="list-unstyled">
            <li class="address" style="color:"""+textcolor+""";">"""+address+"""</li>
            <li class="phone" style="color:"""+textcolor+""";"><a href="tel://"""+phonenumber+"""">"""+phonenumber+"""</a></li>
            <li class="email" style="color:"""+textcolor+""";">"""+email+"""</li>
          </ul>
        </div>


      </div>
    </div>
    <div class="row pt-5 mt-5 text-center">
      <div class="col-md-12">
        <p>
        <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
        Copyright &copy;<script>document.write(new Date().getFullYear());</script> All rights reserved | This template is made with <i class="icon-heart" aria-hidden="true"></i> by <a href="https://colorlib.com" target="_blank" class="text-primary">Colorlib</a>
        <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
        </p>
      </div>

    </div>
  </div>
</footer>
</div>

<script src="static/js/jquery-3.3.1.min.js"></script>
<script src="static/js/jquery-ui.js"></script>
<script src="static/js/popper.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/owl.carousel.min.js"></script>
<script src="static/js/jquery.magnific-popup.min.js"></script>
<script src="static/js/aos.js"></script>
<script src="static/js/main.js"></script>

</body>
</html>"""
