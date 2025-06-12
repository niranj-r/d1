import React from 'react';
import { useNavigate } from 'react-router-dom';
import ProjectDirectory from './ProjectDirectory';

import './styles/AdminDashboard.css';
const AdminDashboard = () => {
  const navigate = useNavigate();

  return (
<div className="admin-dashboard">
  <div className="dashboard-container">
    <div className="dashboard-header">
      <h1>Project Dashboard</h1>
      <p>Welcome! Choose an action below to manage the system.</p>
    </div>

    <div className="dashboard-directory">
      <ProjectDirectory />
    </div>
  </div>
</div>

  );
};

export default AdminDashboard;
