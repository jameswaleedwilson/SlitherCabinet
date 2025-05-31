#version 330 core

in vec3 vertices;
in vec3 vertex_color;
in vec3 vertex_normal;
in vec2 vertex_uv;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform vec4 clip_plane;
//uniform vec4 u_clipPlane = vec4(0.0, 0.0, -1.0, 24.0);

out vec3 color;
out vec3 normal;
out vec3 frag_pos;
out vec3 view_pos;
out vec2 UV;

void main()
{
    view_pos = vec3(inverse(model_mat) *
                    vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2],1));

    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(vertices,1);

    gl_ClipDistance[0] = dot(model_mat * vec4(vertices, 1.0), clip_plane);

    normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
    frag_pos = vec3(model_mat * vec4(vertices,1));
    color = vertex_color;
    UV = vertex_uv;
}