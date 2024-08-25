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
  const uniqueStates = Array.from(new Set(DealersList.map(dealer => dealer.state)));
    setStates(uniqueStates);
    setDealersList(DealersList);
  }, [DealersList]);

  const filterDealers = (state) => {
    if (state === "All") {
      loadDealers();
    } else {
      const filteredDealers = DealersList.filter(dealer => dealer.state === state);
      setDealersList(filteredDealers);
    }
  };

  useEffect(() => {
    loadDealers();
  }, [loadDealers]);

  const isLoggedIn = sessionStorage.getItem("username") != null;

  // Function to handle dealer click and store ID in session storage
  const handleDealerClick = (id) => {
    sessionStorage.setItem("dealerId", id);
    window.location.href = `/dealer/${id}`;
  };

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
              <td><a href="#" onClick={() => handleDealerClick(dealer.id)}>{dealer.full_name}</a></td>
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
