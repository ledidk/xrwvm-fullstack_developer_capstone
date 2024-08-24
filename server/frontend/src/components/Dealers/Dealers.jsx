import React, { useState, useEffect, useCallback } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";
import DealershipDatabase from "../data/dealerships.json";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  const DealersList = DealershipDatabase.dealerships; // Static JSON data

  // Load all dealers and populate state options
  const loadDealers = useCallback(() => {
    // Extract unique states from the static JSON data
    const uniqueStates = Array.from(new Set(DealersList.map(dealer => dealer.state)));
    setStates(uniqueStates); // Populate the state dropdown
    setDealersList(DealersList); // Populate the dealers list with all dealers
  }, [DealersList]);

  // Filter dealers by state
  const filterDealers = (state) => {
    if (state === "All") {
      loadDealers(); // Load all dealers if "All" is selected
    } else {
      const filteredDealers = DealersList.filter(dealer => dealer.state === state);
      setDealersList(filteredDealers); // Update dealers list based on selected state
    }
  };

  // Load all dealers when the component mounts
  useEffect(() => {
    loadDealers();
  }, [loadDealers]);

  const isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header />
      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
                <option value="All">All States</option>
                {states.map((state, index) => (
                  <option key={index} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map(dealer => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td><a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a></td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td>
                  <a href={`/postreview/${dealer.id}`}>
                    <img src={review_icon} className="review_icon" alt="Post Review" />
                  </a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers;
