import React, { useEffect, useState } from "react";
import "./officelocation.css";

import DeckGL from "@deck.gl/react";
import { ScatterplotLayer, LineLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";
import { MapView } from "@deck.gl/core";
import OfficeSelector from "./OfficeSelector/OfficeSelector";

import { loadJSONData } from "../helperfunctions/HelperFunctions";
import OfficeRisk from "./OfficeRisk/OfficeRisk";

// Set your mapbox access token here
const MAPBOX_ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

const Ofx = (props) => {
  // Viewport settings
  const INITIAL_VIEW_STATE = {
    longitude: -122.41669,
    latitude: 37.7853,
    zoom: 13,
    pitch: 0,
    bearing: 0,
  };
  // Data to be used by the LineLayer
  const lineData = [
    {
      sourcePosition: [-122.41669, 37.7853],
      targetPosition: [-122.41669, 37.781],
    },
  ];

  const locationsData = [
    [-122.41669, 37.7853],
    [-122.41669, 37.781],
  ];

  const locationsLayer = new ScatterplotLayer({
    id: "locations-scatterplot-layer",
    locationsData,
    pickable: true,
    opacity: 0.8,
    stroked: true,
    filled: true,
    radiusScale: 6,
    radiusMinPixels: 1,
    radiusMaxPixels: 100,
    lineWidthMinPixels: 1,
    getPosition: (d) => d,
    getRadius: (d) => 100,
    getFillColor: (d) => [255, 140, 0],
    getLineColor: (d) => [0, 0, 0],
  });

  const layers = [new LineLayer({ id: "line-layer-h", lineData })];
  console.log(layers);

  window.deck.log.enable();
  window.deck.log.level = 3;

  return (
    <div className="">
      <div className="  ">
        <DeckGL
          initialViewState={INITIAL_VIEW_STATE}
          viewState={INITIAL_VIEW_STATE}
          controller={true}
          layers={layers}
        >
          {/* <LineLayer id="line-layer" data={lineData} /> */}
          {/* <MapView id="map" width="100%" controller={true}>
            <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
          </MapView> */}
          <LineLayer id="line-layer" data={lineData} />

          <ScatterplotLayer
            id="locations-scatter-plot"
            data={locationsData}
            pickable={true}
            opacity={0.8}
            getPosition={(d) => d}
            getRadius={(d) => 100}
            getFillColor={(d) => [255, 140, 0]}
            getLineColor={(d) => [0, 0, 0]}
          />
        </DeckGL>
      </div>
    </div>
  );
};

// const locationsLayer = new ScatterplotLayer({
//   id: "locations-scatterplot-layer",
//   locationsData,
//   pickable: true,
//   opacity: 0.8,
//   stroked: true,
//   filled: true,
//   radiusScale: 6,
//   radiusMinPixels: 1,
//   radiusMaxPixels: 100,
//   lineWidthMinPixels: 1,
//   getPosition: (d) => d,
//   getRadius: (d) => 100,
//   getFillColor: (d) => [255, 140, 0],
//   getLineColor: (d) => [0, 0, 0],
// });

export default Ofx;
