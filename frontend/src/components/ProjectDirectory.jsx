import React, { useState, useEffect } from 'react';
import './EmployeeDirectory.css';
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import axios from 'axios';

const EmployeeDirectory = () => {
  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/projects');
      setProjects(res.data);
    } catch (err) {
      console.error('Failed to fetch projects', err);
    }
  };

  const handleEdit = (id) => {
    const project = projects.find(p => p._id === id);
    const updated = {
      ...project,
      name: prompt('Edit name', project.name) || project.name,
      email: prompt('Edit email', project.email) || project.email,
      phone: prompt('Edit phone', project.phone) || project.phone,
      joinDate: prompt('Edit join date', project.joinDate) || project.joinDate
    };
    setProjects(prev => prev.map(p => (p._id === id ? updated : p)));
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this project?')) return;
    try {
      await axios.delete(`http://localhost:5000/api/projects/${id}`);
      setProjects(prev => prev.filter(p => p._id !== id));
    } catch (err) {
      console.error('Failed to delete project', err);
    }
  };

  const handleAdd = async () => {
    const name = prompt('Enter name');
    const email = prompt('Enter email');
    const phone = prompt('Enter phone number');
    const joinDate = prompt('Enter join date (YYYY-MM-DD)');
    if (!name || !email || !phone || !joinDate) return;

    try {
      const res = await axios.post('http://localhost:5000/api/projects', {
        name, email, phone, joinDate
      });
      setProjects(prev => [...prev, res.data]);
    } catch (err) {
      console.error('Failed to add project', err);
    }
  };

  const filteredProjects = projects.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="employee-table-container">
      <div className="table-header">
        <h2>Project Page</h2>
        <div className="controls">
          <span>Page 1 of 1</span>
        </div>
      </div>

      <div className="table-header">
        <h2>Project Details</h2>
        <div className="controls">
          <input
            type="text"
            className="search-bar"
            placeholder="Search project..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="add-btn" onClick={handleAdd}>
            <FaPlus /> Add Project
          </button>
        </div>
      </div>

      <table className="employee-table">
        <thead>
          <tr>
            <th>Project ID</th>
            <th>Department ID</th>
            <th>Name</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Budget</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredProjects.map((proj) => (
            <tr key={proj._id}>
              <td>{proj._id}</td>
              <td>{proj.departmentId || '—'}</td>
              <td>{proj.name}</td>
              <td>{proj.startDate || '—'}</td>
              <td>{proj.endDate || '—'}</td>
              <td>{proj.budget || '—'}</td>
              <td>{proj.createdAt || '—'}</td>
              <td>
                <FaEdit className="icon edit-icon" onClick={() => handleEdit(proj._id)} />
                <FaTrash className="icon delete-icon" onClick={() => handleDelete(proj._id)} />
              </td>
            </tr>
          ))}
          {filteredProjects.length === 0 && (
            <tr>
              <td colSpan="8" className="no-data">No matching projects found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default EmployeeDirectory;
