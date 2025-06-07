import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './App.css'
import Root from './common/RootRoute';
import Home from './features/home/routes/Home';
import Login from './features/authentication/components/Login';
import SearchResults from './features/search/components/SearchResults';

import Register from './features/authentication/components/Register';

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Root />,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "results/",
          element: <SearchResults />,
        },
        {
          path: "login/",
          element: <Login />
        },
        {
          path: "/register",
          element: <Register />
        }
      ],
    },
  ]);

  return <RouterProvider router={router} />
}

export default App;
