import React from 'react';

const DynamicForm = ({ schema, formData, setFormData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const renderField = (field) => {
    switch (field.type) {
      case 'text':
        return (
          <div key={field.name}>
            <label>{field.label}</label>
            <input
              type="text"
              name={field.name}
              value={formData[field.name] || ''}
              onChange={handleChange}
            />
          </div>
        );
      case 'textarea':
        return (
          <div key={field.name}>
            <label>{field.label}</label>
            <textarea
              name={field.name}
              value={formData[field.name] || ''}
              onChange={handleChange}
            />
          </div>
        );
      case 'checkbox':
        return (
          <div key={field.name}>
            <label>
              <input
                type="checkbox"
                name={field.name}
                checked={formData[field.name] || false}
                onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked })}
              />
              {field.label}
            </label>
          </div>
        );
      // Add other field types as needed (e.g., select, radio)
      default:
        return null;
    }
  };

  return (
    <div>
      {schema.map(field => renderField(field))}
    </div>
  );
};

export default DynamicForm;
