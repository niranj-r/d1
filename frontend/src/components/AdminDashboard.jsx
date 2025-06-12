import React from 'react';
import { useNavigate } from 'react-router-dom';
import EmployeeDirectory from './EmployeeDirectory';

import './styles/AdminDashboard.css';
const AdminDashboard = () => {
  const navigate = useNavigate();

  return (
<div className="admin-dashboard">
  <div className="dashboard-container">
    <div className="dashboard-header">
      <h1>Admin Dashboard</h1>
      <p>Welcome! Choose an action below to manage the system.</p>
    </div>

    <div className="dashboard-welcome">
      <h3>Quick Actions</h3>
      <div className="dashboard-buttons">
        <button className="dashboard-btn" onClick={() => navigate('/manage-users')}>
          👥 Manage Users
        </button>
        <button className="dashboard-btn1" onClick={() => navigate('/manage-org-dept')}>
          🏢 Manage Organisations
        </button>
        <button className="dashboard-btn2" onClick={() => navigate('/manage-users')}>
          👥 Manage Departments
        </button>
        <button className="dashboard-btn3" onClick={() => navigate('/project-dashboard')}>
          👥 Manage Projects
        </button>
      </div>
    </div>

    <div className="dashboard-directory">
      <EmployeeDirectory />
    </div>
  </div>
</div>

  );
};

export default AdminDashboard;
