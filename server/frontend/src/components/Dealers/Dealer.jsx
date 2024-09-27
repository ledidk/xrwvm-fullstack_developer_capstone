import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';
import ReviewDatabase from "../data/reviews.json"; // Import the reviews data
import DealershipDatabase from "../data/dealerships.json"; // Import the dealership data

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  const params = useParams();
  const id = params.id;

  const DealerList = DealershipDatabase.dealerships; // Load dealership data from the JSON file
  const ReviewList = ReviewDatabase.reviews; // Load review data from the JSON file

  // Define the URLs
  const dealer_url = `/dealer/${id}`; // This is the route you defined for the dealer details page
  const post_review = `/postreview/${id}`; // Define the post review URL

  const get_dealer = () => {
    const dealerData = DealerList.find(dealer => dealer.id === parseInt(id));
    if (dealerData) {
      setDealer(dealerData);
    }
  };
  
  const get_reviews = () => {
    const storedReviews = sessionStorage.getItem("reviews");
    if (!storedReviews) {
      // If not, store the ReviewDatabase in session storage
      sessionStorage.setItem("reviews", JSON.stringify(ReviewList)); // Convert to JSON string
    }

    // Load reviews from session storage
    const sessionReviews = JSON.parse(sessionStorage.getItem('reviews')) || [];
    console.log("HERE ARE sessionReviews", sessionReviews)

    // Ensure sessionReviews is an array
    if (Array.isArray(sessionReviews)) {
      const dealerReviews = sessionReviews.filter(review => review.dealership === parseInt(id));
      

      if (dealerReviews.length > 0) {
        setReviews(dealerReviews);
        console.log("HERE ARE REVIEWS for selected id", dealerReviews)
      } else {
        setUnreviewed(true);
      }
    } else {
      console.error("sessionReviews is not an array:", sessionReviews);
      setUnreviewed(true); // Or handle it as you see fit
    }
  };

  const senti_icon = (sentiment) => {
    let icon = sentiment === "positive" ? positive_icon : sentiment === "negative" ? negative_icon : neutral_icon;
    return icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review}>
          <img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' />
        </a>
      );
    }
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>{dealer.full_name}{postReview}</h1>
        <h4 style={{ color: "grey" }}>{dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}</h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          <text>Loading Reviews....</text>
        ) : unreviewed === true ? <div>No reviews yet! </div> :
          reviews.map(review => (
            <div className='review_panel' key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon" alt='Sentiment' />
              <div className='review'>{review.review}</div>
              <div className="reviewer">{review.name} {review.car_make} {review.car_model} {review.car_year}</div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Dealer;
