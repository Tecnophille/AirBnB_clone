$('document').ready(function() {
  // Fetch API status
  $.get('https://bdbnb.site/api/v1/status/', function(response) {
    if (response.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });

  // Fetch all places
  $.ajax({
    url: 'https://bdbnb.site/api/v1/places_search/',
    type: 'POST',
    data: '{}',
    contentType: 'application/json',
    dataType: 'json',
    success: appendPlaces
  });

  // Dynamically filter states
  let states = {};
  $('.locations > UL > H2 > INPUT[type="checkbox"]').change(function() {
    if ($(this).is(':checked')) {
      states[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete states[$(this).attr('data-id')];
    }
    const locations = Object.assign({}, states, cities);
    if (Object.values(locations).length === 0) {
      $('.locations H4').html('&nbsp;');
    } else {
      $('.locations H4').text(Object.values(locations).join(', '));
    }
  });

  // Dynamically filter cities
  let cities = {};
  $('.locations > UL > UL > LI INPUT[type="checkbox"]').change(function() {
    if ($(this).is(':checked')) {
      cities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete cities[$(this).attr('data-id')];
    }
    const locations = Object.assign({}, states, cities);
    if (Object.values(locations).length === 0) {
      $('.locations H4').html('&nbsp;');
    } else {
      $('.locations H4').text(Object.values(locations).join(', '));
    }
  });

  // Dynamically filter amenities
  let amenities = {};
  $('.amenities INPUT[type="checkbox"]').change(function() {
    if ($(this).is(':checked')) {
      amenities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete amenities[$(this).attr('data-id')];
    }
    if (Object.values(amenities).length === 0) {
      $('.amenities H4').html('&nbsp;');
    } else {
      $('.amenities H4').text(Object.values(amenities).join(', '));
    }
  });

  // Handle search button click event
  $('BUTTON').click(function() {
    $.ajax({
      url: 'https://bdbnb.site/api/v1/places_search/',
      type: 'POST',
      data: JSON.stringify({
        states: Object.keys(states),
        cities: Object.keys(cities),
        amenities: Object.keys(amenities)
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: appendPlaces
    });
  });
});

// Dynamically insert places
function appendPlaces(data) {
  $('SECTION.places').empty();
  $('SECTION.places').append('<H1>Places</H1>');
  $.get('https://bdbnb.site/api/v1/users/', function(response) {
    const users = response;
    for (let place of data) {
      const user = users.find(u => u.id === place.user_id);
      $('SECTION.places').append(
        `<ARTICLE>
          <DIV class="name_and_price">
            <H2>${place.name}</H2>
            <DIV class="price_by_night">
              $${place.price_by_night}
            </DIV>
          </DIV>
          <DIV class="information">
            <DIV class="max_guest">
              <I class="fa fa-users fa-3x" aria-hidden="true"></I>
              </BR>
              ${place.max_guest} Guests
            </DIV>
            <DIV class="number_rooms">
              <I class="fa fa-bed fa-3x" aria-hidden="true"></I>
              </BR>
              ${place.number_rooms} Bedrooms
            </DIV>
            <DIV class="number_bathrooms">
              <I class="fa fa-bath fa-3x" aria-hidden="true"></I>
              </BR>
              ${place.number_bathrooms} Bathrooms
            </DIV>
          </DIV>
          <DIV class="user"><STRONG>Owner: </STRONG>${user.first_name} ${
          user.last_name
        }</div>
          <DIV class="description">
            ${place.description}
          </DIV>
        </ARTICLE>`
      );
    }
  });
}
