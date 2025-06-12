import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';
import ManageUsers from './components/ManageUsers';
import ManageOrgDept from './components/ManageOrgDept';
import AdminSignup from './components/AdminSignup';
import EmployeeDirectory from './components/EmployeeDirectory';
import ProjectDashboard from './components/ProjectDashboard';
import ProjectDirectory from './components/ProjectDirectory';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/admin-dashboard" element={<AdminDashboard />} />
      <Route path="/manage-users" element={<ManageUsers />} />
      <Route path="/manage-org-dept" element={<ManageOrgDept />} />
      <Route path="/admin-signup" element={<AdminSignup />} />
      <Route path="/employee-directory" element={<EmployeeDirectory />} />
      <Route path="/project-dashboard" element={<ProjectDashboard />} />
      <Route path="/project-directory" element={<ProjectDirectory />} />
    </Routes>
  );
}

export default App;
