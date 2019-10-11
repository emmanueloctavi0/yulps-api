import React, { Component } from "react";
import PropTypes from "prop-types";


class ShoppingList extends Component {
    render() {
      return (
        <div className="shopping-list">
          <h1>Shopping List for {this.props.name}</h1>
          <ul>
            <li>Instagram</li>
            <li>WhatsApp</li>
            <li>Oculus</li>
            <li>Github</li>
          </ul>
        </div>
      );
    }
  }

export default ShoppingList;
