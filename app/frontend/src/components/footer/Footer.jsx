/**
 * @license
 * Copyright 2019 Fast Forward Labs.
 * Written by Victor Dibia / Contact : https://github.com/victordibia
 * CaseQA - CaseQA: Question Answering on Large Datasets with BERT.
 * Licensed under the MIT License (the "License");
 * =============================================================================
 */

import React from "react";
import "./footer.css";

const Footer = () => {
  return (
    <div className="border-gray-200 border-l-0 border-r-0 border-b-0  border w-full">
      <div
        style={{ zIndex: 999000 }}
        className=" container-fluid text-gray-500 text-sm w-full p-2"
      >
        Made with <span className="text-red-500">&#9829;</span> at{" "}
        <a
          href="https://www.cloudera.com/products/fast-forward-labs-research.html"
          target="blank"
        >
          Cloudera Fast Forward Labs
        </a>
        .
      </div>
    </div>
  );
};

export default Footer;
