import React from "react";

type Result = {
  title: string;
  institution: string;
  aps: number;
};

const otherResults: Result[] = [
  {
    title: "Computer Science",
    institution: "University of the Witwatersrand",
    aps: 40,
  },
  {
    title: "Computer Science",
    institution: "University of the Witwatersrand",
    aps: 40,
  },
  {
    title: "Computer Science",
    institution: "University of the Witwatersrand",
    aps: 40,
  },
  {
    title: "Computer Science",
    institution: "University of the Witwatersrand",
    aps: 40,
  },
];

export default function SearchResults(){
  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 py-8 space-y-6">
      <div className="w-full max-w-md space-y-6">
        <h2 className="text-xl font-bold text-gray-800">Searched Term</h2>

        <div>
          <p className="text-sm text-gray-500 mb-2">Average Results</p>
          <div className="bg-white rounded-xl shadow-md px-4 py-3 flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-gray-800">Computer Science</h3>
              <p className="text-sm text-gray-500">
                Top Institutions: Wits, UJ, UP, etc
              </p>
            </div>
            <div className="text-sm font-semibold text-gray-700">APS: 35</div>
          </div>
        </div>

        <div>
          <p className="text-sm text-gray-500 mb-2">Other Results</p>
          <div className="space-y-3">
            {otherResults.map((res, index) => (
              <div
                key={index}
                className="bg-white rounded-xl shadow-md px-4 py-3 flex justify-between items-center"
              >
                <div>
                  <h3 className="font-semibold text-gray-800">
                    {res.title}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {res.institution}
                  </p>
                </div>
                <div className="text-sm font-semibold text-gray-700">
                  APS: {res.aps}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-between mt-6">
          <button className="bg-gray-200 text-gray-800 font-semibold py-2 px-6 rounded-full shadow-md hover:bg-gray-300 transition">
            BACK
          </button>
          <button className="bg-blue-500 text-white font-semibold py-2 px-6 rounded-full shadow-md hover:bg-blue-600 transition">
            NEXT
          </button>
        </div>
      </div>
    </div>
  );
};
