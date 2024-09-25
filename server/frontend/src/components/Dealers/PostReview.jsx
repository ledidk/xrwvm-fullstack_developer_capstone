import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

// Import JSON data with different variable names
import CarDatabase from "../data/car_records.json";
import ReviewDatabase from "../data/reviews.json";
import DealershipDatabase from "../data/dealerships.json";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState();
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let params = useParams();
  let id = params.id;

  // Log the ID requested in the URL
  console.log("Requested Dealer ID:", id);

  // Load data from the JSON files
  const CarmodelList = CarDatabase.cars; 
  const ReviewList = ReviewDatabase.reviews; 
  const DealershipList = DealershipDatabase.dealerships; 

  // Fetch dealer info based on the dealership ID
  useEffect(() => {
    const foundDealer = DealershipList.find(dealer => dealer.id === parseInt(id));
    if (foundDealer) {
      setDealer(foundDealer);
    } else {
      console.error("Dealer not found.");
    }

    // Load car models into state
    if (CarmodelList && CarmodelList.length > 0) {
      setCarmodels(CarmodelList);
    } else {
      console.error("No car models found in the JSON.");
    }
  }, [id, DealershipList, CarmodelList]);

  const postReview = () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    if (!model || review === "" || date === "" || year === "" || model === "") {
      alert("All details are mandatory");
      return;
    }

    let model_split = model.split(" ");
    let make_chosen = model_split[0];
    let model_chosen = model_split[1];

    // Create new review object
    let newReview = {
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    };

    console.log("New Review:", newReview);

    // Simulate saving new review to ReviewList
    ReviewList.push(newReview);

    // Log updated reviews
    console.log("Updated Reviews:", ReviewList);

    // Redirect to the dealer page after posting the review
    window.location.href = window.location.origin + "/dealer/" + id;
  }

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
        <div className='input_field'>
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>
        <br />
        <div className='input_field'>
          Car Make
          <select name="cars" id="cars" onChange={(e) => {
              setModel(e.target.value); 
              console.log("Selected Car Model:", e.target.value); // Log selected value
          }}>
              <option value="" selected disabled hidden>Choose Car Make and Model</option>
              {carmodels.map((carmodel, index) => (
                  <option key={index} value={carmodel.make + " " + carmodel.model}>
                      {carmodel.make} {carmodel.model}
                  </option>
              ))}
          </select>
        </div>
        <br />

        <div className='input_field'>
          Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015} />
        </div>

        <div>
          <button className='postreview' onClick={postReview}>Post Review</button>
        </div>
      </div>
    </div>
  );
}

export default PostReview;
