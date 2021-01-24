import React, { useEffect, useState } from "react";
import "./officelocation.css";

import DeckGL from "@deck.gl/react";
// import { LineLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";
import { MapView } from "@deck.gl/core";
import OfficeSelector from "./OfficeSelector/OfficeSelector";

import { loadJSONData } from "../helperfunctions/HelperFunctions";
import OfficeRisk from "./OfficeRisk/OfficeRisk";

// Set your mapbox access token here
const MAPBOX_ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

const OfficeLocations = (props) => {
  const [locations, setLocations] = useState([]);
  const [trends, setTrends] = useState([]);
  const [locationType, setLocationType] = useState("all");

  // Viewport settings
  const INITIAL_VIEW_STATE = {
    longitude: -122.41669,
    latitude: 37.7853,
    zoom: 13,
    pitch: 0,
    bearing: 0,
  };
  // Data to be used by the LineLayer
  // const data = [
  //   {
  //     sourcePosition: [-122.41669, 37.7853],
  //     targetPosition: [-122.41669, 37.781],
  //   },
  // ];

  useEffect(() => {
    const trendsPath = props.selections.serverBasePath + "/trends";
    const locationsPath = props.selections.serverBasePath + "/locations";
    console.log("Trends and Locations Data requested ..");

    let locPromise = loadJSONData(locationsPath);
    locPromise
      .then(function (data) {
        if (data) {
          setLocations(data[locationType]);
        }
      })
      .catch(function (err) {
        console.log("Failed to fetch locations data.", err);
      });

    let trendPromise = loadJSONData(trendsPath);
    trendPromise
      .then(function (data) {
        if (data) {
          setTrends(data);
        }
      })
      .catch(function (err) {
        console.log("Failed to fetch trends data.", err);
      });
  }, [props.selections.serverBasePath]);

  useEffect(() => {
    document.title = `Cloudera Covid Advisor | Locations `;
  }, []);

  return (
    <div className="">
      <div className="  ">
        <DeckGL
          className=""
          initialViewState={INITIAL_VIEW_STATE}
          controller={true}
        >
          <MapView id="map" width="100%" controller={true}>
            <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
          </MapView>
        </DeckGL>
      </div>
      <div className="absolute ml-2 ">
        <OfficeSelector locations={locations} trends={trends} />
        <OfficeRisk locations={locations} trends={trends} />
      </div>
    </div>
  );
};

export default OfficeLocations;
