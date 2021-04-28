import "./main.css";
// import "./main.scss";
import "antd/dist/antd.css";

import { Route, HashRouter } from "react-router-dom";
import Footer from "./footer/Footer";
import Header from "./header/Header";
import OfficeLocations from "./OfficeLocations/OfficeLocations";

function Main() {
  const serverBasePath = window.location.protocol + "//" + window.location.host;
  // const serverBasePath = "http://localhost:5000";
  const selections = { serverBasePath: serverBasePath };
  return (
    <HashRouter>
      <div className="flex flex-col h-screen  ">
        <Header />
        <main className="container-fluid w-full   flex-grow p-2">
          <Route
            exact
            path="/"
            render={(props) => (
              <OfficeLocations {...props} selections={selections} />
            )}
          />
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
}

export default Main;
