import React from "react";
import ReactDOM from "react-dom";
import ShoppingList from "./ShoppingList";

const App = () => (
    <ShoppingList/>
);

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
