var products = [
        {
            'id': 1001,
            'title': 'Soap',
            'price': 3.98,
            'desc': 'Very clean soapy soap, descriptive text'
        },
        {
            'id': 1002,
            'title': 'Grapes',
            'price': 4.56,
            'desc': 'A bundle of grapey grapes, yummy'
        },
        {
            'id': 1003,
            'title': 'Pickles',
            'price': 5.67,
            'desc': 'A jar of pickles is pickly'
        },
        {
            'id': 1004,
            'title': 'Juice',
            'price': 2.68,
            'desc': 'Yummy orange juice'
        }
    ]

/************************************
START of cart operation functions
************************************/

// create add item function to push to Cart
function addItem(id) {
  // clear sessionStorage
  // sessionStorage.clear();

  // check to see if a cart key exisits in sessionStorage
    // if it does, set a local cart variable to work with the parsed string
    // if it does not exist, set an empty array
  if (sessionStorage.getItem('cart')) {
    var cart = JSON.parse(sessionStorage.getItem('cart'));
  }
  else {
    var cart = [];
  }

  // send a response to products.json and create a callback that loops through the products and checks the product id
    // if the product id in the current iteration is the same as the id being taken in as the parameter, then push it to the cart.
  for (let product in products) {
    if (id == products[product].id) {
      cart.push(products[product]);
      break;
    }
  }

  // store to sessionStorage
  sessionStorage.setItem('cart', JSON.stringify(cart));

  showCart();
}


// create a removeCart function that splices the given item
function removeItem(id) {
  // get cart key from sessionStorage and parse it into object
  let cart = JSON.parse(sessionStorage.getItem('cart'));

  // loop through all items in the Cart
    // check if the id passed in is the same as the current items
    // if so, remove it and break
  for (let product in cart) {
    if (cart[product].id == id) {
      cart.splice(product, 1);
      break;
    }
  }

  sessionStorage.setItem('cart',JSON.stringify(cart));

  showCart();
}

// calculating and returning the Total
function calcTotal() {
  // get value and parse sessionStorage
  let cart = JSON.parse(sessionStorage.getItem('cart'));

  // loop through all items in the Cart
    // add each items price to Total
  // return total
  let total = 0;
  for (let product in cart) {
    total += cart[product].price;
  }
  return total.toFixed(2)
}


// updating all classes with total being displayed
function updateTotals() {
  // define a total variable from the return of calcTotal
  // insert into all classes with total
  let total = calcTotal();
  $('.total').text(`$${total}`);

  // convert total to cents
  total = total * 100;
  total = Math.ceil(total);

  // Insert form into id of pay
  let html =`
    <form action="/pay/?amount=${total}" method="POST">
      <script
        src="https://checkout.stripe.com/checkout.js" class="stripe-button"
        data-key="pk_test_j5jUibU8tFHLeLPfUfYzSHNs"
        data-amount="${total}"
        data-name="Joshhall"
        data-description="Widget"
        data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
        data-locale="auto">
      </script>
    </form>
  `
  $('#pay').html(html);
}

function countDuplicates(id) {
  let cart = JSON.parse(sessionStorage.getItem('cart'));
  let count = 0;
  for (let i in cart) {
    if (cart[i].id == id) {
      count += 1;
    }
  }
  return count
}

// create a showCart method to render all items withing the cart variable
function showCart(id) {
  // get value and parse sessionStorage
  let cart = JSON.parse(sessionStorage.getItem('cart'));
  // if cart is empty set the table in the cart col-md-3 section to display none
  if (cart.length === 0) {
    $('#cart-checkout').css('display','none');
    $('#empty').html('<h1>You have no items in your cart.</h1>');
    $('.total').text('Your cart is empty');
  }
  // otherwise show table by setting display to block, loop over all items in cart and create a new row for each item
  else {
    let html = "";

    // send the proper string into the tbody section
    $('#cart').css('display','block');

    let duplicates = [];

    for (let product in cart) {
      let count = countDuplicates(cart[product].id);

      if (duplicates.indexOf(cart[product].id) == -1) {
        html += `
          <tr>
            <td>${count}</td>
            <td>${cart[product].title}</td>
            <td>$${(cart[product].price*count).toFixed(2)}</td>
            <td>
              <button class="btn btn-danger" onclick="removeItem('${cart[product].id}')">X</button>
            </td>
          </tr>
        `;
        duplicates.push(cart[product].id);
      }
    }

    updateTotals();
    $('tbody').html(html);
  }
}

showCart();

/************************************
END of cart operation functions
************************************/
