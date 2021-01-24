import React, { useEffect } from "react";
import "./curate.css";

import DeckGL from "@deck.gl/react";
import { LineLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";
import { MapView, FirstPersonView } from "@deck.gl/core";
import OfficeSelector from "./OfficeSelector/OfficeSelector";

// Set your mapbox access token here
const MAPBOX_ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

const OfficeLocations = () => {
  // Viewport settings
  const INITIAL_VIEW_STATE = {
    longitude: -122.41669,
    latitude: 37.7853,
    zoom: 13,
    pitch: 0,
    bearing: 0,
  };
  // Data to be used by the LineLayer
  const data = [
    {
      sourcePosition: [-122.41669, 37.7853],
      targetPosition: [-122.41669, 37.781],
    },
  ];

  useEffect(() => {
    document.title = `Cloudera Covid Advisor | Locations `;
  }, []);

  return (
    <div className=" h-full">
      {/* <div className="border">FareCalculator</div> */}
      <DeckGL
        className=""
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
      >
        <MapView id="map" width="100%" controller={true}>
          <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
        </MapView>

        <div className="absolute left-4 top-16">
          <OfficeSelector />
        </div>
      </DeckGL>
    </div>
  );
};

export default OfficeLocations;
