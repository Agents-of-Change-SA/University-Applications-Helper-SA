import { useState } from "react";
import {
  Search,
  ChevronRight,
  GraduationCap,
  Pencil,
  Users,
} from "lucide-react";

const Home = () => {
  const [career, setCareer] = useState("");
  const [filter, setFilter] = useState("");

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-100 flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md space-y-6">
        <h1 className="text-2xl font-bold text-center text-yellow-500 mb-4 tracking-tight">
          🎓 Welcome to Univice
        </h1>

        <div className="flex items-center bg-white rounded-2xl shadow-lg px-4 py-3 space-x-3 transition hover:shadow-xl">
          <GraduationCap className="text-yellow-400" />
          <input
            type="text"
            value={career}
            onChange={(e) => setCareer(e.target.value)}
            placeholder="Search Careers"
            className="flex-grow bg-transparent outline-none text-gray-700 placeholder:text-gray-400"
          />
          <Search className="text-gray-600" />
        </div>

        <div className="flex items-center justify-between bg-white rounded-2xl shadow-lg px-4 py-3 transition hover:shadow-xl">
          <div className="flex items-center space-x-3">
            <Pencil className="text-yellow-400" />
            <span className="text-gray-700 font-medium">Filter By</span>
          </div>
          <ChevronRight className="text-yellow-400" />
        </div>

        <button
          onClick={() => console.log("Search")}
          className="w-full bg-yellow-400 text-white font-semibold py-3 rounded-2xl shadow-md hover:bg-yellow-500 transition-all duration-200"
        >
          SEARCH
        </button>

        <div className="flex items-center bg-white rounded-2xl shadow-lg px-4 py-3 space-x-3 transition hover:shadow-xl">
          <Users className="text-yellow-400" />
          <span className="text-gray-700 font-medium">Find Tutors</span>
        </div>
      </div>
    </div>
  );
};

export default Home;
