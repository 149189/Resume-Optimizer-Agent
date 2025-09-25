import FileUpload from "./components/FileUpload";
import MatchTool from "./components/MatchTool";
import SemanticSearch from "./components/SemanticSearch";
import "./App.css";

function App() {
  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <div className="title">Resume Optimizer Agent</div>
          <div>Dev</div>
        </div>
        <div className="card"><FileUpload /></div>
        <div className="card"><MatchTool /></div>
        <div className="card"><SemanticSearch /></div>
      </div>
    </div>
  );
}
export default App;
