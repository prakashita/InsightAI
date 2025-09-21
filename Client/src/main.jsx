import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  createRoutesFromElements,
} from "react-router-dom";
import FileUploader from './Scene/FileUploader.jsx'
import Chat from './Scene/Chat.jsx'

const router= createBrowserRouter(
  createRoutesFromElements(
     <>
    <Route path='/' element={<App/>}>
      <Route path='' element={<FileUploader/>}/>
      <Route path='testchat' element={<Chat/>}/>
    </Route>
    </>
      )
)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)

